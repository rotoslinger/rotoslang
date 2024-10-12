from functools import wraps
import inspect

def initializer(func):
    """
    To avoid the redundancy of creating an arg and then assigning it to an instance variable.
    The idea belongs to Nadia Alramli and was found on stack overflow.
    'varargs' and 'varkw' are the names of the * and ** arguments or None....(taken from inspec.getargspec)
    According to Nadia Alramli:
    Automatically assigns args to instance attributes.
    >>> class process:
    ...     @initializer
    ...     def __init__(self, cmd, reachable=False, user='root'):
    ...         pass
    >>> p = process('halt', True)
    >>> p.cmd, p.reachable, p.user
    ('halt', True, 'root')
    """
    names, varargs, keywords, defaults = inspect.getargspec(func)

    @wraps(func)
    def wrapper(self, *args, **kargs):
        for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
            setattr(self, name, arg)

        for name, default in zip(reversed(names), reversed(defaults)):
            if not hasattr(self, name):
                setattr(self, name, default)

        func(self, *args, **kargs)

    return wrapper
