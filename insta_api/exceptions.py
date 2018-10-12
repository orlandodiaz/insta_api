class LoginAuthenticationError(Exception):
    """Raised when the server fails to authenticate login credentials"""

class InvalidHashtag(Exception):
    """Raised when user entered an invalid hashtag"""

class CheckpointRequired(Exception):
    """ Raised when checkpoint is required"""
