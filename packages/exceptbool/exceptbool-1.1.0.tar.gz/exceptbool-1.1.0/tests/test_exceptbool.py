from pytest import raises

from exceptbool import except_to_bool


def test_except_to_bool_returns_false_when_exception_raised():
    @except_to_bool
    def raise_exception():
        raise Exception()

    assert raise_exception() is False


def test_except_to_bool_returns_true_when_exception_not_raised():
    @except_to_bool
    def do_not_raise_exception():
        return "I will not raise any exceptions, promise!"

    assert do_not_raise_exception() is True


def test_except_to_bool_returns_given_bool_when_given_exception_raised():
    expected_bool = True

    @except_to_bool(exc=IOError, to=expected_bool)
    def raise_exception():
        raise IOError()

    assert raise_exception() is expected_bool


def test_except_to_bool_returns_given_bool_negation_when_given_exception_not_raised():
    expected_bool = False

    @except_to_bool(exc=IOError, to=not expected_bool)
    def do_not_raise_exception():
        return "I will not raise any exceptions, promise!"

    assert do_not_raise_exception() is expected_bool


def test_except_to_bool_returns_given_bool_when_sub_exception_raised():
    expected_bool = True

    @except_to_bool(exc=Exception, to=expected_bool)
    def raise_sub_exception():
        raise AssertionError()

    assert raise_sub_exception() is expected_bool


def test_except_to_bool_does_not_catch_exception_when_exception_different_than_given_exception_raised():
    different_exception = FileNotFoundError

    @except_to_bool(exc=AttributeError)
    def raise_different_exception():
        raise different_exception()

    with raises(different_exception):
        raise_different_exception()


def test_except_to_bool_raises_exception_when_given_exception_is_not_an_exception():
    @except_to_bool(exc=None)
    def raise_runtime_exception():
        raise RuntimeError()

    with raises(TypeError) as exc:
        raise_runtime_exception()
    assert 'catching classes that do not inherit from BaseException is not allowed' in str(exc)


def test_except_to_bool_returns_bool_representation_when_to_is_not_a_bool():
    @except_to_bool(to="")
    def raise_exception():
        raise TimeoutError

    assert raise_exception() is False


def test_except_to_bool_returns_negated_bool_representation_when_to_is_not_a_bool():
    @except_to_bool(to="")
    def do_not_raise_exception():
        return "I will not raise any exceptions, promise!"

    assert do_not_raise_exception() is True


def test_except_to_bool_returns_false_when_one_of_given_exceptions_raised():
    @except_to_bool(exc=(ConnectionError, KeyError))
    def raise_exception():
        raise KeyError()

    assert raise_exception() is False


def test_except_to_bool_returns_true_when_none_of_given_exceptions_raised():
    @except_to_bool(exc=(LookupError, FloatingPointError))
    def do_not_raise_exception():
        return "I will not raise any exceptions, promise!"

    assert do_not_raise_exception() is True


def test_except_to_bool_does_not_catch_exception_when_exception_different_than_given_exceptions_raised():
    different_exception = IndexError

    @except_to_bool(exc=(EOFError, ImportError))
    def raise_different_exception():
        raise different_exception()

    with raises(different_exception):
        raise_different_exception()


def test_except_to_bool_does_not_catch_exception_when_given_exceptions_are_empty_tuple():
    exception = OSError

    @except_to_bool(exc=())
    def raise_exception():
        raise exception()

    with raises(exception):
        raise_exception()


def test_except_to_bool_passes_params_to_decorated_function():
    function_side_effect = []
    positional_param = 34
    keyword_param = 68

    @except_to_bool
    def decorated_function(side_effect, pos_arg, keyword_arg):
        side_effect.append(pos_arg + keyword_arg)

    decorated_function(function_side_effect, positional_param, keyword_arg=keyword_param)

    assert function_side_effect == [positional_param + keyword_param]


def test_except_to_bool_raises_error_when_providing_positional_arguments_to_decorator():
    with raises(TypeError) as error:
        @except_to_bool(None, MemoryError, True)
        def decorated_function():
            pass

    assert 'except_to_bool() takes from 0 to 1 positional arguments but 3 were given' in str(error)


def test_except_to_bool_does_not_change_identity_of_decorated_function():
    @except_to_bool
    def decorated_function():
        """
        This is a decorated function.
        """
        pass

    assert decorated_function.__name__ == 'decorated_function'
    assert 'This is a decorated function.' in decorated_function.__doc__
