import pytest
from insta_api.insta_api import InstaAPI
from tests.testing_config import username, password
from insta_api.utils import media_id_to_code
import time

@pytest.fixture(scope="class")
def insta():
    insta = InstaAPI()
    insta.login(username, password)
    yield insta
    insta._close_session()


class TestInstaAPI:
    """ You must be logged in to run the tests. Login is assumed to work"""




    def test_like(self, insta):
        """ Test the like is working"""


        insta.like('BoLcMrelK4k')

        assert insta.last_resp.ok

    def test_follow_by_name(self, insta):

        insta.follow_by_name('insta_api_user')

        assert insta.last_resp.ok

    def test_unfollow_by_name(self, insta):

        insta.unfollow_by_name('insta_api_user')

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

        photo_resp = insta.last_resp

        # Save the media_id for cleanup
        uploaded_media_id = photo_resp.json()['media']['pk']
        insta.delete_post(uploaded_media_id)

        assert photo_resp.ok
        assert photo_resp.json()['status'] == 'ok'

    def test_delete_post_using_mediaid(self, insta):
        insta.post_photo('../resources/travel.jpeg', 'Delete me')
        media_id = insta.last_resp.json()['media']['pk']
        print(media_id)
        insta.delete_post(media_id)

        assert insta.last_resp.ok

    def test_delete_post_using_shortcode(self, insta):
        insta.post_photo('../resources/travel.jpeg', 'Delete me 2')
        media_id = insta.last_resp.json()['media']['pk']
        print(media_id)
        code = media_id_to_code(media_id)
        insta.delete_post(code)

        assert insta.last_resp.ok

    def test_get_hash_feed(self, insta):
        hashtag_data = insta.get_hash_feed('test')

        assert hashtag_data



