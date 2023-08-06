from typing import Any

class ParamValidator(object):

    @staticmethod
    def assert_not_empty(arg=None, param_name=None):
        # type: (Any, str) -> None
        if ParamValidator.is_empty(arg):
            raise TypeError("Invalid parameter {0}. Cannot be null, empty or consist of whitespace only".
                            format(param_name))

    @staticmethod
    def assert_not_null(arg, param_name=None):
        # type: (Any, str) -> None
        if ParamValidator.is_null(arg):
            raise TypeError("Invalid parameter {0}. Cannot be null.".format(param_name))

    @staticmethod
    def is_empty(arg):
        # type: (Any) -> bool
        if arg is None:
            return True
        elif type(arg) is str or type(arg) is unicode:
            return arg.strip() == ''
        elif type(arg) is int:
            return arg == 0
        elif not arg:
            return True
        else:
            return False

    @staticmethod
    def not_empty(arg):
        # type: (Any) -> bool
        return not ParamValidator.is_empty(arg)

    @staticmethod
    def is_null(arg):
        # type: (Any) -> bool
        return arg is None


