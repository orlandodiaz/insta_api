class LoginAuthentiationError(Exception):
    """Raised when the server fails to authenticate login credentials"""

class InvalidHashtag(Exception):
    """Raised when user entered an invalid hashtag"""