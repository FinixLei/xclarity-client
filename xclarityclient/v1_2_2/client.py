class Client(object):
    def __init__(self, username=None, password=None,
                 version=None, url=None):
        self._version = version
        self._username = username
        self._password = password
        self._url = url

    def info(self):
        print('version: %s' % self._version)
        print('user name: %s' % self._username)
        print('password: %s' % self._password)
        print('url: %s' % self._url)
