from werkzeug.exceptions import BadRequest


class Json(dict):
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            raise BadRequest("Json body required.")

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError as e:
            raise BadRequest('Object key {} is required.'.format(str(e)))
