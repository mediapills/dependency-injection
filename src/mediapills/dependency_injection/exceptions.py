class BaseContainerException(Exception):

    pass


class ExpectedInvokableException(BaseContainerException):  # dead: disable

    pass


class FrozenServiceException(BaseContainerException):

    pass


class InvalidServiceIdentifierException(BaseContainerException):  # dead: disable

    pass


class UnknownIdentifierException(BaseContainerException, KeyError):

    pass


class RecursionInfiniteLoopError(  # dead: disable
    BaseContainerException, RecursionError
):
    pass
