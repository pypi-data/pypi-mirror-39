import requests
import six


# __all__ = ['query']


def _generate_join(collection, local_id, foreign_id):
    """Make join string for query from parameters."""
    text = '{{!join from={fid} to={lid} fromIndex={collection}}}'
    text = text.format(
            collection=collection,
            lid=local_id,
            fid=foreign_id)
    return text


def _generate_query(query):
    """Make query string from query configurations.

    Query syntax is as follows:

        1. A simple query has the following form::

                {field_1: value_1, ..., field_n: value_n}

        in which case the resulting query is::

                q=field1:value_1 AND ... AND fieldn:value_n

        if the value of a field is a list or tuple of strings, the
        generated string ``field:value`` will be replaced with::

                (field:subvalue_1 OR ... OR field:subvalue_k)

        2. A list can be a query if its of the form::

                [
                    {query_1},
                    ...,
                    {query_n}
                ]

        where each object in the list is a valid query. In this case the
        resulting query is::

                q=(query_txt_1) AND ... AND (query_txt_n)

        3. A query is a dict of the type::

                query = {'AND': list_of_queries, ...}

        or::

                query = {'OR': list_of_queries, ...}

        where list of queries is a list as in the previous point.
        Both keys cannot appear at the same time and they define the
        CONJUNCTION operator. Hence if::

                list_of_queries = [{query_1}, ..., {query_n}]

        the resulting query is::

                q=(query_txt_1) CONJUNCTION ... CONJUNCTION (query_txt_n)

        4. If the query is of the previous type, it may have additional fields
        modifying the query, such as:

            a. 'JOIN'.
                Which is a join configuration. See :py:func:`_generate_join`

    Examples
    --------

    Say you want to generate the query::

        q=(
            (field1:user OR field1:curator)
                AND
            (
                (field2:specimen AND field3:*)
                    OR
                (
                    field4:excretes
                        OR
                    field4:print
                        OR
                    field4:remains
                )
            )
                AND
            field4:id
        )

    This is the result of::

        q = _generate_query([
            {field1: ['user', 'curator']},
            {'OR':[
                {fiedl2: 'specimen', field3: '*'},
                {field4: ['excretes', 'print', 'remains']},
            ]},
            {field4: 'id'}
        ])

    """
    # Handle shortcurt format
    if isinstance(query, (list, tuple)):
        query = {'AND': query}

    if not isinstance(query, dict):
        raise ValueError('Query is not a dictionary or list/tuple.')

    # Handle empty query
    if len(query) == 0:
        return '*:*'

    # Handle shortcut format 2
    if ('AND' not in query) and ('OR' not in query):
        query = {'AND': [query]}

    if ('AND' in query) and ('OR' in query):
        msg = 'Query not well formed. Cannot specify AND and OR'
        msg += ' values simultaneously.'
        raise ValueError(msg)

    # Extract the conjunction operator
    if 'AND' in query:
        connector = 'AND'
    else:
        connector = 'OR'

    queries = []
    for subquery in query[connector]:
        if not isinstance(subquery, dict):
            msg = 'Query not well formed. A subquery is not a'
            msg += ' dictionary.'
            raise ValueError

        # Recursive parsing for complex queries
        if ('OR' in subquery) or ('AND' in subquery):
            queries.append(_generate_query(subquery))

        else:
            subqueries = []
            for key, value in six.iteritems(subquery):
                if isinstance(value, dict):
                    msg = 'Query not well formed. A subquery field value '
                    msg += 'cannot be a dictionary.'
                    raise ValueError(msg)

                # Case when subquery is list or tuple. It is assumed that the
                # list or tuple contains the posible values for the key field.
                if isinstance(value, (list, tuple)):
                    subsubqueries = []
                    for subvalue in value:
                        subsubqueries.append(
                            '{key}:{subvalue}'.format(
                                key=key,
                                subvalue=subvalue))
                    subquery_txt = '({})'.format(' OR '.join(subsubqueries))
                    subqueries.append(subquery_txt)

                else:
                    # Final case when a single value is specified for a key
                    # field.
                    subqueries.append(
                        '{field}:{value}'.format(
                            field=key,
                            value=value))

            # Form subquery text with parens if more than one conditions are
            # given
            if len(subquery) > 1:
                subquery_txt = '({})'.format(' AND '.join(subqueries))
            else:
                subquery_txt = subqueries[0]

            queries.append(subquery_txt)

    # Connect all subformulas with the conjunction operator defined in the
    # query.
    query_join = ' {} '.format(connector).join(queries)

    # Form final query with parens in case more than one field is
    # specified.
    if len(queries) > 1:
        query_txt = '({query})'.format(query=query_join)
    else:
        query_txt = queries[0]

    # Add any joining datasets
    if 'JOIN' in query:
        join_data = query['JOIN']

        collection = join_data['collection']
        from_index = join_data['from']
        to_index = join_data['to']

        join_txt = _generate_join(collection, to_index, from_index)

        query_txt = '{join}{query}'.format(join=join_txt, query=query_txt)

    return query_txt


def _generate_facet(config):
    """Make facet string for query from facet configurations.

    A facet configuration is a dictionary with specific fields.

    Facet can be of three types:

    1. field
    2. count
    3. pivot

    There are global configurations for all facet types. These are specified
    in the following fields:

    1. limit
    2. sort
    3. mincount

    For field type facet you must specify the following fields:

    1. field
        Field with which to bucketize documents.

    For range type facet you must specify the following fields:

    1. range
        Field with which to bucketize documents.
    2. start
    3. end
    4. step

    For pivot type facet you must specify the following fields:

    1. pivot
        List of fields with which to bucketize documents.

    For more information of faceting checkout the solr documentation:
    https://lucene.apache.org/solr/guide/6_6/faceting.html

    """
    if config is None:
        config = {}

    if len(config) == 0:
        return ''

    elements = ['facet=true']

    if 'field' in config:
        field = config['field']
        elements.append('facet.field={}'.format(field))

        if 'mincount' in config:
            mincount = config['mincount']
            elements.append('facet.mincount={}'.format(mincount))

    elif 'range' in config:
        field = config['range']
        elements.append('facet.range={}'.format(field))

        start = config['start']
        end = config['end']
        gap = config['gap']

        elements.extend([
            'facet.range.start={}'.format(start),
            'facet.range.end={}'.format(end),
            'facet.range.gap={}'.format(gap),
        ])

        if 'mincount' in config:
            mincount = config['mincount']
            elements.append('facet.mincount={}'.format(mincount))

    elif 'pivot' in config:
        fields = config['pivot']
        elements.append('facet.pivot={}'.format(
            ','.join(fields)))

        if 'mincount' in config:
            mincount = config['mincount']
            elements.append('facet.pivot.mincount={}'.format(mincount))

    if 'limit' in config:
        limit = config['limit']
        elements.append('facet.limit={}'.format(limit))

    if 'sort' in config:
        sortby = config['sort']
        elements.append('facet.sort={}'.format(sortby))

    # TODO check facet documentation to expand options.
    return '&{}'.format('&'.join(elements))


def _generate_group(group):
    """Make group text for query from group configurations.

    A group configuration is a dictionary with following fields:
        1. field
            Field with which to make groups.
        2. query, optional
            Addiontal query to form groups.
        3. limit, optional
            Number of groups to show in result.

    """
    if not isinstance(group, dict):
        msg = 'Group configuration must be a dictionary.'
        raise ValueError(group)

    elements = ['group=true']

    if 'field' not in group:
        msg = 'Group field was not specified'
        raise ValueError(msg)

    field = group['field']
    elements.append('group.field={}'.format(field))

    if 'query' in group:
        query = _generate_query(group['query'])
        elements.append('group.query={}'.format(query))

    if 'limit' in group:
        limit = group['limit']
        elements.append('group.limit={}'.format(limit))

    return '&{}'.format('&'.join(elements))


def _generate_collapse(collapse):
    """Make collapse string for query from collapse configurations.

    A collapse configuration is a dictionary with following fields:
        1. field
            Field with which to collapse results.
        2. null_policy, optional
            Policy with which to handle missing data
        3. size, optional
            Number of documents per group to show in result.

    """
    if 'field' not in collapse:
        msg = 'Field is not specified in collapse configuration.'
        raise ValueError(msg)

    options = ['field={}'.format(collapse['field'])]

    if 'null_policy' in collapse:
        null_policy = collapse['null_policy']
        options.append('nullPolicy={}'.format(null_policy))

    if 'size' in collapse:
        size = collapse['size']
        options.append('size={}'.format(size))

    base_string = '{{!collapse {options}}}'
    return base_string.format(options=' '.join(options))


def query(
        host,
        collection,
        query=None,
        extra='',
        facet=None,
        rows=None,
        start=None,
        group=None,
        additional_queries=None,
        collapse=None,
        frmt='json',
        fq=None,
        fl=None):
    """Make query to solar and return results.

    Parameters
    ----------
    host : str
        Host name of solr server
    collection : str
        Collection from which to query
    query : dict, optional
        Query configuration. See :py:func:`_generate_query`. If
        no query is provided, all documents will be returned (limited by the
        rows argument).
    extra : str, optional
        A string to be appended to the query url. Defaults to empty string.
    facet : dict, optional
        Facet configuration. See :py:func:`_generate_facet`. If no facet
        configuration is provided no facet will be included.
    rows : int, optional
        Number of documents to return from query. Defaults to 10.
    start : int, optional
        Index of document at which to start querying. Defaults to 0.
    group : dict, optional
        Group configuration. See :py:func:`_generate_group`. If no group
        configurations are provided no grouping will occur.
    additional_queries : dict or list or tuple, optional
        Single or mutiple queries to add.
    collapse : dict, optional
        Collapse configuration. See :py:func:`_generate_collapse`. If no
        collapse configurations are provided no collapse will occur.
    frmt : str, optional
        Format of solr response. Defaults to json.
    fq : dict, optional
        Query configuration to use as filter query parameter. See
        :py:func:`_generate_query`. If no configuration is provided no filter
        query will be used.
    fl : list or tuple, optional
        Field list parameter. Only fields included in this list will be
        returned by solr.

    Returns
    -------
    data : frmt
        Solar response in the desired format (frmt)

    """
    base_url = '{host}/solr/{collection}/select?q={query}'

    # Handle empty query
    if query is None:
        query = {'*': '*'}

    # Turn query into text
    query = _generate_query(query)

    # Form basic query url
    base_url = base_url.format(
        host=host,
        collection=collection,
        query=query)

    # Add requested output format to query url
    if frmt == 'json':
        extra += '&wt=json'

    # Add facet configurations to query url
    extra += _generate_facet(facet)

    # Add any additional queries
    if additional_queries is not None:
        if not isinstance(additional_queries, (list, tuple)):
            additional_queries = [additional_queries]

        for add_query in additional_queries:
            add_query = _generate_query(add_query)
            extra += '&q={}'.format(add_query)

    # Add row limit to query url
    if rows is not None:
        extra += '&rows={}'.format(rows)

    # Add starting row to query url
    if start is not None:
        extra += '&start={}'.format(start)

    # Add filter query to query url
    if fq is not None:
        fq = _generate_query(fq)

    # Add collapse option to query url
    if collapse is not None:
        collapse = _generate_collapse(collapse)

        if fq is not None:
            fq = collapse + fq
        else:
            fq = collapse

    if fq is not None:
        extra += '&fq={}'.format(fq)

    # Add field list to filter response fields to query url
    if fl is not None:
        fl = ','.join(fl)
        extra += '&fl={}'.format(fl)

    # Add grouping to query url
    if group is not None:
        extra += _generate_group(group)

    # Add extra fields to query
    query_url = base_url + extra

    # Request data
    request = requests.get(query_url)

    # Parse data and handle errors
    data = request.json()

    return data
