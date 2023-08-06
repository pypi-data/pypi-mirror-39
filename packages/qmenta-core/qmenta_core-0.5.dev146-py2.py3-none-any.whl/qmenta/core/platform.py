import requests
from urllib.parse import urljoin

from .errors import Error

"""
Handles all the communication with the QMENTA platform.
"""


class PlatformError(Error):
    """
    When there is a problem in the communication with the platform.
    """
    pass


class ConnectionError(PlatformError):
    """
    When there was a problem setting up the connection with QMENTA platform.
    """
    pass


class InvalidResponseError(PlatformError):
    """
    The QMENTA platform returned an unexpected response.
    """
    pass


class ActionFailedError(PlatformError):
    """
    When the requested action was not successful.
    """
    pass


class InvalidLoginError(ActionFailedError):
    """
    When the provided credentials are incorrect, or when the used token
    is not valid.
    """
    pass


class ChooseDataError(ActionFailedError):
    """
    When a trying to start an analysis, but data has to be chosen

    Parameters
    ----------
    warning : str
        Warning message returned by the platform
    data_to_choose : str
        Specification of the data to choose returned by the platform
    analysis_id : int
        The ID of the analysis for which data needs to be chosen,
        returned by the platform.
    """
    def __init__(self, warning, data_to_choose, analysis_id):
        self.warning = warning
        self.data_to_choose = data_to_choose
        self.analysis_id = analysis_id


class Auth:
    """
    Class for authenticating to the platform.
    Do not use the constructor directly, but use the login() function to
    create a new authentication

    Attributes
    ----------
    base_url : str
        The base URL of the platform. Example: 'https://platform.qmenta.com'
    token : str
        The authentication token, returned by the platform when logging in.
    """
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self._session = None

    @classmethod
    def login(cls, username, password, base_url='https://test.qmenta.com'):
        """
        Authenticate to the platform using username and password.

        Parameters
        ----------
        username : str
            The username to log in on the platform. For all new platform
            accounts, this is the e-mail address of the user.
            Example: 'tim@qmenta.com'
        password : str
            The QMENTA platform password of the user.
        base_url : str
            The URL of the platform to connect to.
            Default value: 'https://platform.qmenta.com'

        Raises
        ------
        ConnectionError
            If there was a problem setting up the network connection with the
            platform.
        InvalidResponseError
            If the platform returned an invalid response.
        InvalidLoginError
            If the login was invalid. This can happen when the
            username/password combination is incorrect, or when the account is
            not active.
        """
        if not base_url.startswith('https://'):
            raise ConnectionError('Base url must start with https://')

        url = urljoin(base_url, '/login')
        try:
            r = requests.post(
                url, data={'username': username, 'password': password}
            )
        except requests.RequestException as e:
            raise ConnectionError(e)

        try:
            d = parse_response(r)
        except ActionFailedError as e:
            raise InvalidLoginError(str(e))

        try:
            token = d['token']
        except KeyError as e:
            raise InvalidResponseError('Missing key: {}'.format(e))

        return cls(base_url, token)

    def get_session(self):
        if not self._session:
            self._session = requests.Session()
            self._session.headers.update(self._headers())

        return self._session

    def _headers(self):
        h = {
            'Cookie': 'AUTH_COOKIE={}'.format(self.token),
            'Mint-Api-Call': '1'
        }
        return h


def parse_response(response):
    """
    Convert a platform response to JSON and check that it is valid.
    This function should be applied to the output of post().

    Parameters
    ----------
    response : requests.Response
        The response from the platform

    Raises
    ------
    InvalidResponseError
        When the response of the platform cannot be converted to JSON,
        or when it has unexpected values or missing keys.
    ActionFailedError
        When the requested action could not be performed by the platform
    ChooseDataError
        When a POST was done to start an analysis, but data needs to be
        chosen before the analysis can be started.

    Returns
    -------
    dict or list
        When the platform returns a response with a list in the JSON, it
        is returned. Otherwise, it is assumed that the returned value is a
        dict. In case the dict has a 'data' key, the value of data in the
        dict is returned, otherwise the full dict is returned.
    """
    try:
        d = response.json()
    except ValueError:
        raise InvalidResponseError(
            'Could not decode JSON for response {}'.format(response))

    if isinstance(d, dict):
        try:
            success = d['success']
            if success == 0:
                errmsg = d['error']
                raise ActionFailedError(errmsg)
            elif success == 1:
                # Good!
                pass
            elif success == 2:
                # You have to choose data
                raise ChooseDataError(
                    warning=d['warning'],
                    data_to_choose=d['data_to_choose'],
                    analysis_id=d['analysis_id']
                )
            elif success == 3:
                errmsg = d['message']
                raise ActionFailedError(errmsg)
            else:
                raise InvalidResponseError(
                    'Unexpected value for success: {}'.format(success)
                )
        except KeyError as e:
            raise InvalidResponseError('Missing key: {}'.format(e))

        try:
            result = d['data']
        except KeyError:
            result = d

    elif isinstance(d, list):
        # In some cases, the platform does not return a dict with additional
        #   information, but only a list with the results.
        result = d
    else:
        raise InvalidResponseError(
            'Response is not a dict or list: {}'.format(response.text))

    return result


def post(auth, endpoint, data={}, headers={}, stream=False):
    """
    Post the given data and headers to the specified platform's endpoint.

    Parameters
    ----------
    auth : qmenta.core.platform.Auth
        Auth object that was used to authenticate to the QMENTA platform
    endpoint : str
        The end-point in the platform to post to
    data : dict
        The data to post
    headers : dict
        The headers to post
    stream : bool
        Stream the response. This is used when downloading files.
        Default value: False.

    Raises
    ------
    qmenta.core.platform.ConnectionError
        When there is a problem connecting to the QMENTA platform

    Returns
    -------
    requests.Response
        The response object returned by the request.
    """
    url = urljoin(auth.base_url, endpoint)
    try:
        # TODO: Add timeout, see IF-1110
        r = auth.get_session().post(
            url=url,
            data=data,
            headers=headers,
            stream=stream
        )
    except requests.RequestException as e:
        raise ConnectionError(e)

    return r
