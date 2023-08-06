#
# 帮助更好的编写命令行工具
#
import os
import sys
from functools import wraps
from termcolor import colored


class Error(Exception):
    pass


class EnvironError(Error):
    def __init__(self, variable, message=None):
        self.variable = variable
        if message is None:
            message = f'Error: 环境变量 `{variable}` 未设置'


def error(text):
    print(
        colored(text, 'red', attrs=['bold']),
        file=sys.stdout)


def warn(text):
    print(
        colored(text, 'red'),
        file=sys.stdout)


def environ_required(*environ_args, **environ_kargs):
    '''  examples:

        [root@localhost]# export A=3
        [root@localhost]# export B=4

        @environ_required('A', b='B')
        def main():
            print(A, b)

        # [out] 3 4

    '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            environ_kargs.update({i: i for i in environ_args})
            for arg, environ_name in environ_kargs.items():
                try:
                    f.__globals__[arg] = os.environ[environ_name]
                except KeyError as e:
                    raise EnvironError(environ_name)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
