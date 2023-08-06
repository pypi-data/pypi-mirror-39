from copy import deepcopy
from urllib.parse import quote, urljoin, urlencode
from itertools import chain


def merge_fields(request):
    # Return a mixture of all provided objects in request
    data = {}
    data.update(request.values.to_dict())
    data.update(request.get_json(force=True, silent=True) or {})
    return deepcopy(data)


def create_url(base, *query, path=None, params={}):
    """ Create a url.

    Creates a url by combining base, path, and the query's list of
    key/value pairs. Escaping is handled automatically. Any
    key/value pair with a value that is None is ignored.

    Keyword arguments:
    base -- The left most part of the url (ex. http://localhost:5000).
    path -- The path after the base (ex. /foo/bar).
    query -- A list of key value pairs (ex. [('key', 'value')]).

    Example usage:
    >>> create_url(
    ...     'http://localhost:5000',
    ...     ('key1', 'value'),
    ...     ('key2', None),     # Will not include None
    ...     ('url', 'http://example.com'),
    ...
    ...     path='foo/bar',
    ...     key=['value1', 'value2']
    ...
    ... )
    'http://localhost:5000/foo/bar?key1=value&url=http%3A%2F%2Fexample.com&key=value1&key=value2'
    """
    url = base
    # Add the path to the url if it's not None.
    if path is not None:
        url = urljoin(url, quote(path))
    # Remove key/value pairs with None values.
    query = chain(
        filter(lambda pair: pair[1] is not None, query), params.items())

    def seperate(entry):
        if isinstance(entry[1], list):
            return ((entry[0], i) for i in entry[1] if i)
        elif entry[1] is None:
            return ()
        return (entry,)
    query = list(chain(*map(seperate, query)))
    # Add the query string to the url
    url = urljoin(url, '?{0}'.format(urlencode(list(query))))
    return url
