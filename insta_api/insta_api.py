import time
import requests
from requests import RequestException
from requests_toolbelt import MultipartEncoder
from json import JSONDecodeError
from requests.models import Response
from log3 import log
import pickle
import os
import insta_api.server_errors
from insta_api.server_errors import *

if __name__ == '__main__':
    from endpoints import *
    # from config import log
    from utils import login_required, logout_required, code_to_media_id, generate_boundary
    from exceptions import (LoginAuthenticationError, InvalidHashtag, CheckpointRequired, MissingMedia, ActionBlocked,
                            IncompleteJSON, NoCookiesFound)

else:
    from .endpoints import *
    # from .config import log
    from .utils import login_required,logout_required, code_to_media_id, generate_boundary
    from .exceptions import (LoginAuthenticationError, InvalidHashtag, CheckpointRequired, MissingMedia, ActionBlocked,
                             IncompleteJSON, NoCookiesFound)

class InstaAPI:

    def __init__(self, use_cookies=True):
        """ Initialization loads cookies by default so no login will be required unless needed"""

        self.ses = requests.Session()

        # self.ses.verify = "charles-ssl-proxying-certificate.pem"
        self.ses.headers = {
            'Accept': '*/*',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Language': 'en-US',
            'referer': 'https://www.instagram.com/',
            'x-instagram-gis': 'x_instagram_gis',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36'
        }
        self.user_data = None

        self.last_resp = None
        self.status = None
        self.msg = None
        self.username = None
        self.use_cookies=use_cookies

        if os.path.isfile('cookies') and use_cookies:
            self._load_cookies()
            self.get_username()
            self._get_init_csrftoken()
            log.info('Logged in as {}'.format(self.username))

    @login_required
    def get_username(self):
        """ Get the current username"""

        if not self.username:
            resp = self._make_request(current_user_endpoint, params={'__a': '1'})
            user_info = resp.json()['form_data']
            username = user_info['username']
            self.username = username

    @property
    def is_loggedin(self):
        """ Check if user is logged in

        Returns: bool: True if logged in, False otherwise.
        """
        return 'sessionid' in self.ses.cookies.get_dict()

    def _load_cookies(self):
        """ Check if there are cookies saved to save on login API calls"""

        if os.path.isfile('cookies'):
            log.debug('Loading cookies')
            with open('cookies', 'rb+') as file:
                cookies = pickle.load(file)
                log.debug('STORED COOKIE: {}'.format(cookies.get_dict()))
                self.ses.cookies = cookies
        else:
            raise NoCookiesFound("No cookies found in the current directory")

    def _save_cookies(self):
        """ Save cookies locally """

        with open('cookies', 'wb+') as file:
            log.debug('Saving cookies {}'.format(self.ses.cookies.get_dict()))
            pickle.dump(self.ses.cookies, file)

        log.debug("SESSION COOKIES: {}".format(self.ses.cookies.get_dict()))

    def _make_request(self, endpoint, data=None, params=None, msg='', post=False):
        """ Shorthand way to make a request.

        Args:
            endpoint (str): API endpoint
            data (dict, None): Data if using POST request
            params (dict, None): Params, if needed
            msg (str): Message to log when response is successful
            post (bool): True if this is a POST request, FALSE otherwise

        Returns:
            Response: Requests response object

        """

        resp = None
        try:
            if not data and not post:
                resp = self.ses.get(base_endpoint + endpoint, headers=self.ses.headers, params=params)
                resp.raise_for_status()
            else:
                resp = self.ses.post(base_endpoint + endpoint, data=data,
                                     headers=self.ses.headers, allow_redirects=False)
                resp.raise_for_status()

        except RequestException as ex:
            if len(resp.text) > 300:
                log.error('STATUS: {} - CONTENT: {}'.format(resp.status_code, resp.text))
            else:
                log.error('STATUS: {} - CONTENT: {}'.format(resp.status_code, resp.text))

            self.last_resp = resp
            self.status = resp.status_code
            self.msg = resp.content
            raise
        else:
            if len(resp.text) > 300:
                log.success('STATUS: {} - CONTENT (truncated): {}'.format(resp.status_code, resp.text[:300]+"..."))
            else:
                log.success('STATUS: {} - CONTENT: {}'.format(resp.status_code, resp.text))            # log.info(msg)

            self.last_resp = resp
            self.status = resp.status_code
            self.msg = resp.content

            return resp

    def _close_session(self):
        """ Closes the request session"""

        self.ses.close()

    def _get_init_csrftoken(self):
        """ Get initial csrftoken from the main website.

        If already logged in, maybe because of a cookie, copy that cookie to the headers
        The csrf token is needed to be in the headers for most API calls"""

        if not self.is_loggedin:
            visit_resp = self._make_request('', msg='Visit was successful.')
            assert 'csrftoken' in visit_resp.cookies.get_dict()
            self.ses.headers.update({'x-csrftoken': visit_resp.cookies['csrftoken']})

        else:
            self.ses.headers.update({'x-csrftoken': self.ses.cookies.get_dict()['csrftoken']})


        # log.debug("Session headers: {}".format(self.ses.headers))
        # log.debug("Cookies: {}".format(self.ses.cookies.get_dict()))

    @logout_required
    def login(self, username, password):
        """Login to instagram.

        Args:
            username (str): Your instagram username
            password (str): Your instagram password

        Raises:
            LoginAuthenticationError: Raised when authentication has failed
            CheckpointRequired: Raised when instagram has detected an unusual login attempt. This usually happens
            when your IP is different or your mid (MACHINE_ID) cookie has changed
        """

        self._get_init_csrftoken()

        login_data = {'username': username, 'password': password}

        try:
            log.info("Logging in as {}".format(username))
            self._make_request(login_endpoint, data=login_data, msg="Login request sent")
        except requests.exceptions.HTTPError:


            resp_data = self.last_resp.json()
            if resp_data['message'] == 'checkpoint_required':

                self._save_cookies()

                checkpoint_url = resp_data['checkpoint_url']
                checkpoint_id = checkpoint_url.split("/")[2]
                checkpoint_code = checkpoint_url.split("/")[3]

                self._make_request(checkpoint_url)

                log.debug(challenge_endpoint.format(id=checkpoint_id, code=checkpoint_code))
                self._make_request(challenge_endpoint.format(id=checkpoint_id, code=checkpoint_code),
                                                             data={'choice':'1'})

                msg = """
                Instagram has flagged this login as suspicious. You are either signing in from an unknown IP
                or your machine id (mid) has changed.
                Please enter the six-digit code that was sent to your instagram registered email to proceed.
                """
                log.error(msg)

                while True:
                    verification_code = input("Enter the six-digit verification code. Type REPLAY to request another one: ")

                    if verification_code == 'REPLAY':
                        self._make_request(challenge_replay.format(id=checkpoint_id, code=checkpoint_code), post=True)
                    else:
                        self._make_request(challenge_endpoint.format(id=checkpoint_id, code=checkpoint_code), data={'security_code': verification_code})
                        break

                if self.is_loggedin:
                    log.info('Logged in successfully')

                    # Store cookies
                    with open('cookies', 'wb+') as file:
                        log.debug('Saving cookies {}'.format(self.ses.cookies.get_dict()))
                        pickle.dump(self.ses.cookies, file)
                else:
                    raise LoginAuthenticationError
        else:
            resp_data = self.last_resp.json()

            if resp_data['authenticated']:
                log.info('Logged in successfully')
                self.ses.headers.update({'x-csrftoken': self.last_resp.cookies['csrftoken']})
                assert 'sessionid' in self.ses.cookies.get_dict()
                self._save_cookies()
                self.username = username

            else:
                raise LoginAuthenticationError

    @login_required
    def like(self, inpt):
        """ Like a single post. media_id or shortcodee"""

        media_id = inpt

        if isinstance(inpt, str) and not inpt.isdigit():
            media_id = code_to_media_id(inpt)
            log.debug(media_id)

        try:
            self._make_request(like_endpoint.format(media_id=media_id), post=True, msg='Liked %s' % media_id)
        except requests.HTTPError as e:
            if e.response.text == 'missing media':
                raise MissingMedia("The post you are trying to like has most likely been removed")

            if e.response.status_code == 400 and e.response.text == action_blocked['text']:
                raise ActionBlocked(" This action was blocked")
            else:
                raise
        except requests.RequestException:
            raise

    @login_required
    def unlike(self, inpt):
        """ Like a single post. media_id or shortcode"""

        media_id = inpt
        if isinstance(inpt, str) and not inpt.isdigit():
            media_id = code_to_media_id(inpt)

        self._make_request(unlike_endpoint.format(media_id=media_id), post=True, msg='Unliked %s' % media_id)

    @login_required
    def follow_by_id(self, user_id):
        """ Follow an user by their unique id, not their username!"""

        print(self.ses.cookies.get_dict())
        self._make_request(follow_endpoint.format(user_id=user_id), post=True, msg='Followed %s' % user_id)

    @login_required
    def follow(self, username):
        """ Follow an user by their unique username"""

        self.follow_by_id(self.get_user_info(username)['id'])

    @login_required
    def follow_by_name(self, username):
        """ Follow an user by their unique username"""

        self.follow_by_id(self.get_user_info(username)['id'])

    @login_required
    def unfollow_by_id(self, user_id):
        """ Unfollow an user by their unique id, not their username!"""

        print(self.ses.cookies.get_dict())
        self._make_request(unfollow_endpoint.format(user_id=user_id), post=True, msg='Unfollowed %s' % user_id)

    @login_required
    def unfollow_by_name(self, username):
        """ Unfollow an user by their unique username"""

        self.unfollow_by_id(self.get_user_info(username)['id'])

    @login_required
    def get_hash_feed(self, hashtag, pages=4):
        """ Get hashtag feed

        Args:
            hashtag (str): The hashtag to be used. Ex. #love, #fashion, #beautiful, etc
            pages (int): The number of pages to crawl. Recommended to not go above four
        Returns:
            dict: Hashtag dictionary containing information about a specific hash

        """

        params = {
            'query_hash': get_hashinfo_query,
            'variables': '{"tag_name": "%s", "first": %d}' % (hashtag, pages)
        }

        resp = self._make_request(graphql_endpoint, params=params, msg='Hash feed was received')

        try:
            data = resp.json()  # => Possible JSONDecoderror
        except JSONDecodeError:
            # Server might return incomplete JSON response or requests might be truncating them.
            # The content-length does not match in some instances
            log.warning('Received an incomplete JSON response')
            raise IncompleteJSON
        else:
            if not data['data']['hashtag']:
                raise InvalidHashtag("Received no data for hashstag. Please make sure it was entered properly")

            return data['data']['hashtag']['edge_hashtag_to_media']['edges']

    @login_required
    def get_user_info(self, username):
        """  Gets information about an user

        Args:
            username (str): The actual literal username
        Returns:
            dict: JSON decoded response
        """

        resp = self._make_request(user_info_endpoint.format(username=username), msg='User info data received')
        return resp.json()['graphql']['user']

    @login_required
    def get_user_info_by_id(self, user_id):
        """ Gets information about an user

        Args:
            user_id (int): The user_id of the user.
        Returns:
            dict: JSON decoded response

        """

        params = {
            'query_hash': get_userinfo_query,
            'variables': '{"user_id": "%s", "include_chaining": true, "include_reel": true,'
                         ' "include_suggested_users": false, "include_logged_out_extras": false,'
                         ' "include_highlight_reels": false}' % user_id
        }

        resp = self._make_request(graphql_endpoint, params=params, msg='User info data received')

        self.user_data = resp.json()['data']['user']['reel']['owner']

        return resp.json()

    @login_required
    def post_photo(self, photo_path, caption="No caption"):
        """ Post a photo to your feed

        Args:
            photo_path (str): Path to photo
            caption (str): The caption for the photo to be posted

        Examples:
            in this case 'beach.jpg' is a file located in the current working directory::

                insta.post_photo('beach.jpg', caption="Swimming in the beach")

        """

        with open(photo_path, 'rb') as photo:
            upload_id = str(int(time.time() * 1000))

            data = {'upload_id': upload_id,
                    'photo': ('photo.jpg', photo, 'image/jpeg')}

            boundary = generate_boundary()

            m = MultipartEncoder(data, boundary="----WebKitFormBoundary%s" % boundary)

            self.ses.headers.update(
                {
                    # 'origin': 'https://www.instagram.com',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'x-requested-with': 'XMLHttpRequest',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36',
                    'x-instagram-ajax': '43b4c36c01b8',
                    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary%s' % boundary,
                    'referer': 'https://www.instagram.com/create/style/',
                }
            )

            resp = self._make_request(post_photo_endpoint1, m.to_string(), 'Uploaded photo successfully')
            upload_id = resp.json()['upload_id']

            self.ses.headers.update({
                'content-type': 'application/x-www-form-urlencoded',
                'referer': 'https://www.instagram.com/create/details/',
            })

            data = [
                ('upload_id', str(upload_id)),
                ('caption', caption),
            ]

            self._make_request(post_photo_endpoint2, data, msg='Photo uploaded was successfully published')

    @login_required
    def delete_post(self, inpt):
        """  Delete a post.

        Args:
            inpt (str, int): inpt can take media_id or shortcode of post
        """

        media_id = inpt
        if isinstance(inpt, str) and not inpt.isdigit():
            media_id = code_to_media_id(inpt)

            self._make_request(delete_endpoint.format(media_id=media_id), post=True, msg='Deleted %s' % media_id)
        else:
            self._make_request(delete_endpoint.format(media_id=media_id), post=True, msg='Deleted %s' % media_id)

    def logout(self):
        """ Logout current user. All other API calls will not work after this method is called"""

        try:
            self._make_request(logout_endpoint, 'Logged out successfully')
        except requests.exceptions.HTTPError:
            self.ses.cookies.update({'sessionid': None})
            # os.remove('cookies')


if __name__ == '__main__':
    # Play with the API here
    pass
