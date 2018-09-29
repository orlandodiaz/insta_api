from insta_api.insta_api import InstaAPI
from .testing_config import username, password

class TestEntry:

    def setup(self):
        self.a = 5
        self.insta = InstaAPI()

    def teardown(self):
        self.insta.close_session()

    def test_visit_status(self):
        """Test visit status code"""
        self.visit_resp = self.insta._make_request('', None, None, 'Visit was successful.')
        assert self.visit_resp.ok

    def test_visit_response_cookies(self):
        """Test whether expected cookie values are present"""
        self.visit_resp = self.insta._make_request('', None, None, 'Visit was successful.')
        assert 'csrftoken' in self.visit_resp.cookies.get_dict()

    def test_login_status(self):
        """ You must be successfully logged in to test the endpoints"""
        self.insta.login(username, password)
        assert self.insta.last_resp.status_code == 200