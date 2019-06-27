from werkzeug.exceptions import Unauthorized


class Authorization:
    def __init__(self, **params):
        self._params = params

    def __iter__(self):
        return iter((self._params.get('username', self._params.get('token')), self._params.get('password')))

    def __getitem__(self, item):
        try:
            return self._params[item]
        except KeyError:
            raise Unauthorized('No auth header for {}'.format(item))

    @property
    def token(self):
        return self['token']

    @property
    def username(self):
        return self['username']

    @property
    def password(self):
        return self['password']
