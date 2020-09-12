class RELEASEPROVISIONException(Exception):
    pass


class SenderError(RELEASEPROVISIONException):
    pass


class ListenerMsgError(RELEASEPROVISIONException):
    pass


class ValidateError(RELEASEPROVISIONException):
    pass
