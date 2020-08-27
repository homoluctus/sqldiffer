class SqlDifferException(Exception):
    """Base Exception"""


class InvalidDbCredentialError(SqlDifferException):
    """Raised when specified db credentials is invalid"""

    msg = 'Invalid server credentials'

    def __init__(self) -> None:
        super().__init__(self.msg)


class DbConnectError(SqlDifferException):
    """Raised when failed to connect to db"""
