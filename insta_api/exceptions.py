class LoginAuthenticationError(Exception):
    """ Raised when the server fails to authenticate login credentials

    Status code and content:
        200: {"authenticated": false, "user": true, "status": "ok"}

    """


class InvalidHashtag(Exception):
    """ Raised when user entered an invalid hashtag

    Status code and content:
        200: {"data":{"hashtag":null},"status":"ok"}

    """


class CheckpointRequired(Exception):
    """ Raised when checkpoint is required

    Status code and content:
       400:  {"message": "checkpoint_required", "checkpoint_url": "/challenge/id/shortcode/", "lock": false, "status": "fail"}

    """


class MissingMedia(Exception):
    """ Raised when the post one is trying to like or follow does not exist (maybe deleted)

    Status code and Text:
       400: missing media

    """


class ActionBlocked(Exception):
    """ Raised when a request was blocked by instagram

    Status code and message:
        400: It looks like you were misusing this feature by going too fast. You’ve been temporarily blocked from using it.
        400: This action was blocked. Please try again later (deprecated)
        429 - {"message": "rate limited", "status": "fail"} (not tested)

    """


class ServerError(Exception):
    """ Raised when other server errors occur

    Status code and message:
        502: HTML doc...
        503: HTML doc...
        500: Oops, an error occurred.


    """


class IncompleteJSON(Exception):
    """ Raised when instagram returns an incomplete JSON, for whatever reason"""


class NoCookiesFound(Exception):
    """ Raised when no cookies are found in the system"""

