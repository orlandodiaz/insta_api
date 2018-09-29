from functools import wraps
import string
import random
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not args[0].is_loggedin:
            raise ValueError('Login required for endpoint')
        return fn(*args, **kwargs)
    return wrapper

def code_to_media_id(shortcode):
    """ Converts shortcode to media_id"""

    alphabet = {char:i for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_')}

    media_id = 0
    for char in shortcode:
        media_id = media_id * 64 + alphabet[char]

    return media_id

def generate_boundary():
    letters = string.ascii_letters+string.digits
    boundary = ''
    for i in range(0, 16):
        boundary+=random.choice(letters)
    return boundary
