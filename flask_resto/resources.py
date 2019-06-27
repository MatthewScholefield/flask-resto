from flask_resto.misc import recursive_merge


class Resources:
    """Class to represent url routes"""
    def __init__(self, val, api):
        self.val = val
        self.api = api

    def update(self, *args, **kwargs):
        self.val.update(*args, **kwargs)
        if self.api._get_app():
            if args:
                assert len(args) == 1
                assert not kwargs
                val = args[0]
            else:
                val = kwargs
            self.apply()

    def apply(self):
        if self.api._get_app():
            self.api._set_resource('', self.val)

    def set(self, val):
        self.val = dict(recursive_merge(self.val, val))
        self.apply()
