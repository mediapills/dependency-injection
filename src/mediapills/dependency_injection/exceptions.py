class BaseInjectorException(Exception):

    pass


class ExpectedInvokableException(BaseInjectorException):

    pass


class FrozenServiceException(BaseInjectorException):

    pass


class ProtectedServiceException(BaseInjectorException):

    pass


class UnknownIdentifierException(BaseInjectorException, KeyError):

    pass


class RecursionInfiniteLoopError(BaseInjectorException, RecursionError):

    pass
