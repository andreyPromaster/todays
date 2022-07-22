class AuthBaseException(Exception):
    """Base class of auth exceptions"""


class PasswordSecuryException(AuthBaseException):
    """Raise if user password is too easy"""


class UserAlreadyExistsException(AuthBaseException):
    """Raise if user create the same account"""


class AccessDeniedException(AuthBaseException):
    """Raise if authentication was failed"""
