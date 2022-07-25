class CRUDBaseException(Exception):
    """Base class of crud exceptions"""


class FieldIsNotUniqueException(CRUDBaseException):
    """Raise when required field is not unique"""


class FieldDoesNotExistException(CRUDBaseException):
    """Raise when required field does not exist"""
