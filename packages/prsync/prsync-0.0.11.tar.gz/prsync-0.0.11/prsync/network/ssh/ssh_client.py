import paramiko


class SSHClient():

    def __init__(self, host="", username="", password=""):
        self._client = None
        self._host = host
        self._username = username
        self._password = password

    def _get_host(self):
        return self._host

    def _set_host(self, host):
        self._host = host

    def _get_username(self):
        return self._username

    def _set_username(self, username):
        self._username = username

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = password

    def new_session(self):
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connection.connect(hostname=self.host, username=self.username,
                           password=self.password)
        self.client = connection

    def _get_client(self):
        return self._client

    def _set_client(self, c):
        self._client = c

    host = property(_get_host, _set_host)
    username = property(_get_username, _set_username)
    password = property(_get_password, _set_password)
    client = property(_get_client, _set_client)

