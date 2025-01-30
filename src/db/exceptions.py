class DBException(Exception):
    pass


class NoDatabaseException(DBException):
    pass


class DatabaseAuthException(DBException):
    pass


class DatabaseConnectionException(DBException):
    pass
