from insta_api.insta_api import InstaAPI
import time
import os
from tests.testing_config import username, password
import pytest
import time


@pytest.fixture(scope="class")
def insta():
    insta = InstaAPI()
    insta.login(username, password)
    yield insta
    insta.close_session()

class TestInstaAPI:
    """ You must be logged in to run the tests. Login is assumed to work"""


    def test_like(self, insta):
        """ Test the like is working"""


        insta.like('BoLcMrelK4k')

        assert insta.last_resp.ok

    def test_follow_by_name(self, insta):
        print(insta.ses.cookies.get_dict())

        insta.follow_by_name('insta_api_user')

        assert insta.last_resp.ok

    def test_unlike(self, insta):
        """ Test the like is working"""
        insta.unlike('BoLcMrelK4k')

        assert insta.last_resp.ok

    def test_get_user_info(self, insta):
        """ Test if user information retrievel is working fine"""

        data = insta.get_user_info('insta_api_tester')
        assert data

    def test_upload_photo(self, insta):
        insta.post_photo('../resources/travel.jpeg', 'no caption')
        assert insta.last_resp.ok

    def test_delete_post(self, insta):
        insta.delete_post(1876730039681510757)
        assert insta.last_resp.ok

    # def test_logout(self, insta):
    #     resp = insta.logout()
    #     assert insta.last_resp.ok

    def test_get_hash_feed(self, insta):
        hashtag_data = insta.get_hash_feed('test')

        assert hashtag_data


