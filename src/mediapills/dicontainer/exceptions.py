class BaseContainerException(Exception):

    pass


class BaseContainerKeyException(KeyError):

    pass


class ExpectedInvokableException(BaseContainerException):  # dead: disable

    pass


class FrozenServiceException(BaseContainerException):

    pass


class InvalidServiceIdentifierException(BaseContainerException):  # dead: disable

    pass


class UnknownIdentifierException(BaseContainerKeyException):

    pass
