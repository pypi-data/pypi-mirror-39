
'''
    类似于 lru_cache, 但提供限时的缓存
'''
from datetime import datetime, timedelta
import functools


def timed_cache(maxsize=128, typed=False, **timedelta_kwargs):
    def _wrapper(f):
        update_delta = timedelta(**timedelta_kwargs)
        next_update = datetime.utcnow() - update_delta
        f = functools.lru_cache(maxsize, typed)(f)

        @functools.wraps(f)
        def _wrapped(*args, **kwargs):
            nonlocal next_update
            now = datetime.utcnow()
            if now >= next_update:
                f.cache_clear()
                next_update = now + update_delta
            return f(*args, **kwargs)
        return _wrapped
    return _wrapper


def counted_cache(count, maxsize=128, typed=False):
    '''
        When count is zero, cache was cleared each time function
        was called, so basically means no cache.
    '''
    def _wrapper(f):
        counter = 0
        f = functools.lru_cache(maxsize, typed)(f)

        @functools.wraps(f)
        def _wrapped(*args, **kwargs):
            nonlocal counter
            res = f(*args, **kwargs)
            if counter < count:
                counter += 1
            else:
                f.cache_clear()
                counter = 0
            return res
        return _wrapped
    return _wrapper


if __name__ == '__main__':
    import time

    @counted_cache(1)
    def test():
        return datetime.now()

    for i in range(10):
        time.sleep(0.1)
        print(i, test())
