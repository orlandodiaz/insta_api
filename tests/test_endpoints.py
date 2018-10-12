import pytest
from insta_api.insta_api import InstaAPI
from insta_api.endpoints import *


@pytest.fixture(scope="module")
def insta():
    insta = InstaAPI()
    yield insta
    insta._close_session()


class TestEndpoints:
    """ These tests make sure that the API endpoints are still reachable and not moved"""

    def test_base_endpoint(self, insta):
        resp = insta.ses.head(base_endpoint)
        assert resp.status_code != 404


    def test_login_endpoint(self, insta):
        resp = insta.ses.head(base_endpoint+login_endpoint)
        assert resp.status_code != 404

        
    def test_upload_photo_endpoint(self, insta):
        resp = insta.ses.head(base_endpoint+post_photo_endpoint1)
        assert resp.status_code != 404

    def test_exploretag_endpoint(self, insta):
        resp = insta.ses.head(base_endpoint + explore_tag.format(hashtag="test"))
        assert resp.status_code != 404

    def test_like_endpoint(self, insta):

        resp = insta.ses.head(base_endpoint + like_endpoint.format(media_id='_'))
        assert resp.status_code != 404

    def test_follow_endpoint(self, insta):
        resp = insta.ses.head(base_endpoint+follow_endpoint.format(user_id="0"))
        assert resp.status_code != 404

    def test_unfollow_endpoint(self, insta):
        resp = insta.ses.head(base_endpoint+unfollow_endpoint.format(user_id="0"))
        assert resp.status_code != 404

    def test_graphql_endpoint(self, insta):
        resp = insta.ses.head(base_endpoint+graphql_endpoint)
        assert resp.status_code != 404

    def test_logout_endpoint(self, insta):
        resp = insta.ses.head(base_endpoint+logout_endpoint)
        assert resp.status_code != 404




   

