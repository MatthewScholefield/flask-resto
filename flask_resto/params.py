from werkzeug.exceptions import BadRequest


class Params(dict):
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError as e:
            raise BadRequest('Parameter {} is required.'.format(str(e)))
