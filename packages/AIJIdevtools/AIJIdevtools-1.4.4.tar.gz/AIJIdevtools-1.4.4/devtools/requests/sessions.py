from requests import Session


class JwtSession(Session):
    token = ''

    def __init__(self, server, username="lvda", password="secret",
                 auth_url='/auth'):
        self.server = server
        self.username = username
        self.password = password
        self.auth_url = server + auth_url
        super().__init__()

    def get_token(self):
        data = {
            "username": self.username,
            "password": self.password,
        }
        resp = super().request(
            'POST', self.auth_url, data=data)
        if resp.status_code == 200:
            self.token = resp.json()['access_token']
        else:
            raise ConnectionError

    def request(self, method, url, **kwargs):
        kwargs['headers'] = {"Authorization": f"JWT {self.token}"}
        url = self.server + url
        resp = super().request(method, url, **kwargs)
        if resp.status_code == 401:
            self.get_token()
            kwargs['headers']["Authorization"] = f"JWT {self.token}"
            resp = super().request(method, url, **kwargs)
        return resp
