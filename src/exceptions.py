

class SecuredServerException(Exception):
    """ The Base class for all Secured Server Exception """
    pass

class InvalidToken(SecuredServerException):
    """
    Provided Token is invalid or has expired.
    """
    pass