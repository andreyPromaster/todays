class CRUDBaseException(Exception):
    """Base class of crud exceptions"""


class WrongModelFieldException(CRUDBaseException):
    """Raise if required field is wrong for current operation"""
