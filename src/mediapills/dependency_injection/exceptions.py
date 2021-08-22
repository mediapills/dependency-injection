class BaseInjectorException(Exception):

    pass


class ExpectedInvokableException(BaseInjectorException):  # dead: disable

    pass


class FrozenServiceException(BaseInjectorException):

    pass


class ProtectedServiceException(BaseInjectorException):

    pass


class InvalidServiceIdentifierException(BaseInjectorException):

    pass


class UnknownIdentifierException(BaseInjectorException, KeyError):

    pass


class RecursionInfiniteLoopError(  # dead: disable
    BaseInjectorException, RecursionError
):
    pass
