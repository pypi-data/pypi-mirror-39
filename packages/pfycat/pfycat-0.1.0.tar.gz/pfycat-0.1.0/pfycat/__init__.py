import requests
import time
import uuid
import time

log_responses = False
log_requests = False
log_waiting = False


def l(o):
    print(o)


class PfycatError(Exception):
    pass


class _Endpoints:
    _base = "https://api.gfycat.com/v1"
    token = _base + "/oauth/token"
    gfycats = _base + "/gfycats"
    status = _base + "/gfycats/fetch/status"
    users = _base + "/users"
    me = _base + "/me"
    file_drop = "https://filedrop.gfycat.com"


class Client:

    def __init__(self, client_id=None, client_secret=None, user_name=None, user_pass=None, timeout_seconds=2 * 60 * 60,
                 retries_on_error=3, wait_s_after_error=5 * 60):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = user_name
        self.password = user_pass
        self.access_token = None
        self.timeout = timeout_seconds
        self.retries_on_error = retries_on_error
        self.wait_s_after_error = wait_s_after_error

        if client_id is None \
                and client_secret is None \
                and user_name is None \
                and user_pass is None:
            self.auth_type = None
        elif client_id and client_secret \
                and user_name is None \
                and user_pass is None:
            self.auth_type = 'client_credentials'
            self._update_access_token()
        elif client_id and client_secret and user_name and user_pass:
            self.auth_type = 'password'
            self._update_access_token()
        else:
            raise PfycatError("authentication uses either all 4 variables, "
                              "only client_id and client_secret, or none.")

    def __call__(self, *args, **kwargs):
        pass

    def me(self):
        url = _Endpoints.me
        return self._get(url)

    def users(self, name):
        return self._get(_Endpoints.users + '/' + name)

    def gfycats(self, gfy_id):
        return self._get(_Endpoints.gfycats + '/' + gfy_id)

    def upload(self, file_path, create_params=None):
        if create_params is None: create_params = {}

        create_respons = self.create_empty_gfycat(create_params)
        if not create_respons['isOk']:
            raise PfycatError('not ok', create_respons)
        # create_secret = create_respons['secret']

        gfyname = create_respons['gfyname']
        self._drop_file(gfyname, file_path)

        status = self.check_status(gfyname)

        while status["task"].lower() == "encoding":
            if log_waiting: l("encoding...")
            time.sleep(2)
            status = self.check_status(gfyname)

        if status["task"] == "complete":
            return status
        elif status["task"] == "NotFoundo":
            raise PfycatError("gfy not foundo after upload", status)
        else:
            raise PfycatError("unknown status: " + status["task"], status)

    def _run_repeatedly(self, fun):
        for i in range(0, self.retries_on_error):
            try:
                return fun()
            except Exception(e):
                l(e)
                l("error, but trying again after waiting...")

                time.sleep(self.wait_s_after_error)
        raise RuntimeError("Aborted after " + str(self.retries_on_error) + " tries.")

    def _drop_file(self, gfyname, file_path):
        with open(file_path, 'rb') as file:
            r = self._run_repeatedly(lambda: requests.put(
                _Endpoints.file_drop + "/" + gfyname,
                data=file,
                timeout=self.timeout))
        if r.status_code != 200:
            raise PfycatError("error while uploading: " + str(r.status_code) + ", " + r.text)
        if log_responses: l(r)
        return r

    def check_status(self, gfyname):
        url = _Endpoints.status + '/' + gfyname
        return self._get(url)

    def create_empty_gfycat(self, create_params=None):
        if create_params is None: create_params = {}
        url = _Endpoints.gfycats
        return self._post(url, self.access_token, json=create_params)

    @classmethod
    def _handle_result(cls, r):
        if log_responses: l(r.text)
        if r.status_code != 200:
            raise PfycatError('bad response', r.status_code, r.text)
        response = r.json()
        if 'error' in response:
            raise PfycatError(response['error'])
        return response

    def _get_auth_header(self):
        if self.access_token:
            if self.auth_type == 'client_credentials':
                return {"Authorization": "Bearer " + self.access_token}
            elif self.auth_type == 'password':
                return {"Authorization": "Bearer " + self.access_token}
            else:
                raise PfycatError("impossible situation. please contact developer")
        else:
            return {}

    def _get(self, url, params=None):
        r = self._run_repeatedly(
            lambda: requests.get(url, params=params, headers=self._get_auth_header(), timeout=self.timeout))

        print("get...")
        if r.status_code == 401 and self.access_token:
            print("refreshing token...")
            # try again with new token
            self._update_access_token()
            r = self._run_repeatedly(lambda: requests.get(url, params=params, headers=self._get_auth_header(), timeout=self.timeout))

        return self._handle_result(r)

    def _post(self, url, data=None, json=None):
        r = self._run_repeatedly(lambda: requests.post(url, data=data, json=json, headers=self._get_auth_header(), timeout=self.timeout))
        if r.status_code == 401 and self.access_token:
            # try again with new token
            self._update_access_token()
            r = self._run_repeatedly(lambda: requests.post(url, data=data, json=json, headers=self._get_auth_header(), timeout=self.timeout))

        return self._handle_result(r)

    def _update_access_token(self):
        """
        {
            "grant_type":"password",
            "client_id":"{{client_id}}",
            "client_secret":"{{client_secret}}",
            "username":"{{username}}",
            "password":"{{password}}"
          }
        :return:
        """

        if self.auth_type is None:
            return
        elif self.auth_type == 'client_credentials':
            params = {'grant_type': 'client_credentials',
                      'client_id': self.client_id,
                      'client_secret': self.client_secret}
        elif self.auth_type == 'password':
            params = {'grant_type': 'password',
                      'client_id': self.client_id,
                      'client_secret': self.client_secret,
                      'username': self.username,
                      'password': self.password
                      }
        else:
            raise PfycatError("impossible situation. please contact developer")

        r = self._run_repeatedly(lambda: requests.post(_Endpoints.token, json=params, timeout=self.timeout))
        if r.status_code != 200:
            raise PfycatError('can\'t get oauth-token', r.status_code, r.text)
        response = r.json()
        if 'error' in response:
            raise PfycatError(response['error'])
        self.access_token = response['access_token']
