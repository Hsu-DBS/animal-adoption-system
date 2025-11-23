from math import ceil

def paginate_query(query, page: int, limit: int):

    if page < 1:
        raise ValueError("page must be >= 1")
    
    if limit < 1:
        raise ValueError("limit must be >= 1")

    total = query.count()
    offset = (page - 1) * limit

    query_data = query.offset(offset).limit(limit).all()

    data_to_return = {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": ceil(total / limit),
        "query_data": query_data
    }

    return data_to_return