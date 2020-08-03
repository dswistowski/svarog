from unittest.mock import Mock

from svarog.dispatchers.functional import FunctionalDispatch
from svarog.dispatchers.multi import MultiDispatcher


def test_functional_dispatcher_should_call_default_handler():
    default = Mock()
    type = Mock()
    data = Mock()
    forge = Mock()
    fb = FunctionalDispatch(default)

    fb(type, data, forge)
    default.assert_called_once_with(type, data, forge)


def test_functional_dispatcher_should_call_handler_based_on_check():
    default = Mock()
    odd_handler = Mock()
    even_handler = Mock()
    forge = Mock()
    fb = FunctionalDispatch(default)

    def is_odd(type):
        return type % 2 == 1

    def is_even(type):
        return type % 2 == 0

    fb.register(is_odd)(odd_handler)
    fb.register(is_even)(even_handler)

    fb(2, "foo", forge)
    fb(1, "bar", forge)

    even_handler.assert_called_once_with(2, "foo", forge)
    odd_handler.assert_called_once_with(1, "bar", forge)

    default.assert_not_called()


def test_multi_dispatcher_will_dispatch_for_registered_type():
    md = MultiDispatcher()
    handle_class = Mock()
    forge = Mock()

    class A:
        pass

    class B(A):
        pass

    md.register_cls(A, handle_class)
    md.dispatch(B)(B, "data", forge)

    handle_class.assert_called_once_with(B, "data", forge)


def test_multi_dispatcher_will_dispatch_for_registered_func():
    md = MultiDispatcher()
    handle_func = Mock()
    forge = Mock()

    class A:
        pass

    def is_a(type):
        return type == A

    md.register_func(is_a, handle_func)
    md.dispatch(A)(A, "data", forge)

    handle_func.assert_called_once_with(A, "data", forge)
