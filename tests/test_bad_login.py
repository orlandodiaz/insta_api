from insta_api.insta_api import InstaAPI
from tests.testing_config import username, password
import time
import pytest
from insta_api.exceptions import LoginAuthenticationError

def test_bad_login():
    insta = InstaAPI()

    with pytest.raises(LoginAuthenticationError):
        insta.login('INVALID_USERNAME', 'INVALID_PASSWORD')



