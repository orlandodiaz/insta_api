from insta_api.insta_api import InstaAPI
from tests.testing_config import username, password
import time


def test_logout():
    insta = InstaAPI(use_cookies=False)
    insta.login(username, password)
    time.sleep(3)

    insta.logout()

    assert insta.last_resp.ok
    assert not insta.is_loggedin
