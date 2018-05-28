import math

__version__ = '0.0.3'


class Page(object):

    def __init__(self, items, page, page_size, limit, total):
        if total < limit:
            limit = total
        self.items = items
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < limit
        if self.has_next:
            self.next_page = page + 1
        self.total = total
        self.pages = int(math.ceil(limit / float(page_size)))


def paginate(query, page, page_size, limit=None):
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        raise AttributeError('page_size needs to be >= 1')
    if limit is not None and limit <= 0:
        raise AttributeError('If limit is set, it needs to be >=1')
    # Limit limits the maximum amount of results allowed
    if limit is not None and page * page_size > limit:
        page = int(limit / page)
        page_size = limit - (page * page_size)
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    # We remove the ordering of the query since it doesn't matter for getting a count and
    # might have performance implications as discussed on this Flask-SqlAlchemy issue
    # https://github.com/mitsuhiko/flask-sqlalchemy/issues/100
    total = query.order_by(None).count()
    if limit is None:
        limit = total
    return Page(items, page, page_size, limit, total)
