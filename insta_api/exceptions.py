class LoginAuthenticationError(Exception):
    """Raised when the server fails to authenticate login credentials"""


class InvalidHashtag(Exception):
    """Raised when user entered an invalid hashtag"""


class CheckpointRequired(Exception):
    """ Raised when checkpoint is required"""


class MissingMedia(Exception):
    """ Raised when the post one is trying to like or follow does not exist (maybe deleted)

    Text:
        missing media

    """


class ActionBlocked(Exception):
    """ Raised when a request was blocked by instagram
    Status code and message:
        400: It looks like you were misusing this feature by going too fast. You’ve been temporarily blocked from using it.
    """


class IncompleteJSON(Exception):
    """ Raised when instagram returns an incomplete JSON, for whatever reason"""


class NoCookiesFound(Exception):
    """ Raised when no cookies are found in the system"""


class ServerError(Exception):
    """ Raised when other server errors occur """

