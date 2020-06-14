from insta_api.insta_api import InstaAPI
import pytest
from insta_api.exceptions import LoginAuthenticationError, NoResponseError


def test_bad_login():
  insta = InstaAPI(use_cookies=False)

  with pytest.raises((LoginAuthenticationError, NoResponseError)):
    insta.login('INVALID_USERNAME', 'INVALID_PASSWORD')
