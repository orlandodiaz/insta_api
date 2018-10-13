class LoginAuthenticationError(Exception):
    """Raised when the server fails to authenticate login credentials"""


class InvalidHashtag(Exception):
    """Raised when user entered an invalid hashtag"""


class CheckpointRequired(Exception):
    """ Raised when checkpoint is required"""


class MissingMedia(Exception):
    """ Raised when the post one is trying to like or follow does not exist (maybe deleted) """


class ActionBlocked(Exception):
    """ Raised when a request was blocked by instagram"""
