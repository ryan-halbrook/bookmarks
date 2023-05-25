def build_sql_where(query, params={}, add_where=True):
    if params and any(params.values()) and add_where:
        query += ' WHERE '
    queryParams = []
    for (key, param) in params.items():
        if not param:
            continue
        if queryParams:
            query += ' AND '
        query += (key + ' = ?')
        queryParams.append(param)
    return query, tuple(queryParams)
