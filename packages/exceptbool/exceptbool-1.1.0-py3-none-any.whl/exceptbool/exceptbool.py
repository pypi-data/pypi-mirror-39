from functools import wraps


def except_to_bool(_func=None, *, exc=Exception, to=False):
    """
    Makes decorated function return bool instead of raising an exception by
    converting given exception(s) into given bool value.

    If no exception will be raised, then negation of given bool will be returned.
    If exception different than given one will be raised, then it will not be caught.

    :param _func: filled automatically by decorator with decorated function -
                  DO NOT fill this param manually
    :param exc: exception(s) to catch and convert; defaults to Exception
    :type exc: BaseException or tuple(BaseException)
    :param to: value to which caught exception will be converted and returned;
               defaults to False
    :type: bool
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return not to
            except exc:
                return bool(to)
        return wrapper
    return decorator(_func) if _func else decorator
