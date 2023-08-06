def to_str(sth):
    if isinstance(sth, str):
        return sth
    elif isinstance(sth, bytes):
        return sth.decode()
    else:
        return str(sth)


def to_bytes(sth):
    if isinstance(sth, bytes):
        return sth
    elif isinstance(sth, str):
        return sth.encode()
    else:
        return bytes(sth)


def to_addr(strs):
    host = 'localhost'
    port = 0
    if isinstance(strs, list):
        if len(strs) == 1:
            return to_addr(strs[0])
        elif len(strs) == 2:
            host = strs[0]
            port = int(strs[1])
        else:
            raise ValueError
        return (host, port)
    elif isinstance(strs, str):
        strs = strs.split(':')
        if len(strs) == 1:
            host = strs[0]
            return (host, port)
        elif len(strs) == 2:
            return to_addr(strs)
        else:
            raise ValueError
    else:
        raise ValueError
