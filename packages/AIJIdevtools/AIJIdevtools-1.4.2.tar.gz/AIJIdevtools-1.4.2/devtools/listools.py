def partition(ls, size):
    """
    Returns a new list with elements
    of which is a list of certain size.

        >>> partition([1, 2, 3, 4], 3)
        [[1, 2, 3], [4]]
    """
    return [ls[i:i+size] for i in range(0, len(ls), size)]


def split(ls, sep=None):
    """
    Split a list by sep

        >>> split([1, None, None, 2, 3, None, 4])
        [[1], [2, 3], [4]]
    """
    res = []
    tmplist = []
    for elem in ls:
        if elem == sep:
            if tmplist:
                res.append(tmplist)
            tmplist = []
        else:
            tmplist.append(elem)
    else:
        res.append(tmplist)
    return res


def dict_ordered(ls, sep='\n', line_prefix=''):
    ls = sorted(ls)
    pre = ls[0][0]
    res = line_prefix + repr(ls[0]) + ','
    for s in ls[1:]:
        if s[0] == pre:
            res += ' ' + repr(s) + ','
        else:
            res += sep + line_prefix + repr(s) + ','
        pre = s[0]
    return res


if __name__ == '__main__':
    l = (
            'id', 'module_id', 'type', 'name', 'status_code',
            'status', 'flow_record', 'flow_nodes',
            'opinions', 'apply_type', 'manager', 'chinese_name',
            'app_level', 'desc', 'lang', 'gitlab', 'dependency_version',
            'basic_software', 'container', 'container_ver',
            'has_container', 'deploy_path', 'log_path',
            'script_path', 'heartbeat_path', 'running_params', 'port',
            'created_time', 'updated_time', 'app_id', 'names'
        )


    print('(\n'+dict_ordered(l, line_prefix=' '*12)+'\n'+' '*8+')')

#     l = '''

# '''
#     l = l.split('\n\n\n')
#     print('\n\n\n'.join(sorted(l)))