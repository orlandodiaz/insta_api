from insta_api.insta_api import InstaAPI
from tests.testing_config import username, password
import pytest
import os


@pytest.fixture(scope="module")
def insta():
    if os.path.isfile('cookies'):
        os.remove('cookies')
    insta = InstaAPI(use_cookies=False)
    yield insta
    insta.logout()


    if os.path.isfile('cookies'):
        os.remove('cookies')

    insta._close_session()


def teardown():
    os.system('say teardown')

    if os.path.isfile('cookies'):
        os.remove('cookies')


def test_save_cookies(insta):
    """ Test if the cookies are being correctly saved"""
    insta._make_request(endpoint='')
    insta._save_cookies()

    assert os.path.isfile('cookies')


def test_load_cookies(insta):
    """ Test if cookies are loaded correctly"""

    insta._make_request(endpoint='')
    insta._save_cookies()

    insta._load_cookies()

    assert insta.ses.cookies






