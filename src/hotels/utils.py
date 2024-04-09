from typing import List, Tuple


def paginate(items, limit, page_number) -> Tuple[List, int, int]:
    start_index: int = (page_number - 1) * limit
    end_index: int = start_index + limit
    pages: int = len(items) // limit
    if (len(items) % limit) != 0:
        pages += 1
    return items[start_index:end_index], pages, len(items)
