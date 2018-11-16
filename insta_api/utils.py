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


def logout_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if args[0].is_loggedin:
            raise ValueError('Logout required before logging in')
        return fn(*args, **kwargs)
    return wrapper


def media_id_to_code(media_id):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    short_code = ''
    while media_id > 0:
        remainder = media_id % 64
        media_id = (media_id-remainder)//64
        short_code = alphabet[remainder] + short_code
    return short_code


def code_to_media_id(shortcode):
    """ Converts shortcode to media_id"""

    alphabet = {char: i for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_')}

    media_id = 0
    for char in shortcode:
        media_id = media_id * 64 + alphabet[char]

    return media_id


def generate_boundary():
    letters = string.ascii_letters+string.digits
    boundary = ''
    for i in range(0, 16):
        boundary += random.choice(letters)
    return boundary
