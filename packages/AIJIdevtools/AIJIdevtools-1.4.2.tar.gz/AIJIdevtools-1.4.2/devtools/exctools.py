def mute(cond, default=None):
    '''
    if `cond` is true, catch all exceptions a function throw
    and if any exception, return the `default` value.
    '''
    def dec(func):
        if cond:
            def f(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    return default
            return f
        else:
            return func
    return dec
