import flask
import json
import re
import traceback
from base64 import b64decode
from flask import Flask, has_app_context, request
from functools import wraps
from werkzeug.exceptions import HTTPException, BadRequest

from flask_resto.authorization import Authorization
from flask_resto.json import Json
from flask_resto.params import Params
from flask_resto.resources import Resources


class Api:
    """Core api object"""
    METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    def __init__(self, app: Flask = None):
        self._resources = Resources({}, self)
        self.app = app
        if app:
            self.init_app(app)
        self.routes = {}

    def init_app(self, app: Flask):
        self.app = app
        self._resources.apply()
        self.app.add_url_rule('/', 'index', self._index, methods=['GET'])
        self.app.add_url_rule('/endpoints', 'endpoints', self._endpoints, methods=['GET'])

    @property
    def resources(self):
        """Get the currently registered url routes"""
        return self._resources.val

    @property
    def params(self):
        """Get the url parameters (ie. ?key1=val&key2=val2)"""
        return Params(request.args)

    @property
    def json(self):
        """Parse json data from body if header is set"""
        data = request.get_json()
        if data is None:
            raise BadRequest('Json data required')
        return Json(data)

    @property
    def auth(self):
        """Parse basic / bearer auth from headers"""
        t, value = request.headers.get('Authorization', ' ').split(' ')
        if t == 'Basic':
            username, password = b64decode(value).decode().split(':')
            return Authorization(username=username, password=password)
        elif t == 'Bearer':
            return Authorization(token=value)
        else:
            return Authorization()

    @resources.setter
    def resources(self, val: dict):
        """Assign url routes to the api"""
        self._resources.set(val)

    def _endpoints(self):
        """Gets a swagger representation of all the endpoints"""
        var_pattern = r'<(|string:|int:|float:|path:|uuid:)([a-zA-Z_]+)>'
        paths = {}
        res = self._resources.val
        vals = [([route], val) for route, val in res.items()]
        while vals:
            new_vals = []
            for route, val in vals:
                if isinstance(val, dict):
                    for k, v in val.items():
                        new_vals.append((route + [k], v))
                else:
                    *route_parts, method = route
                    func = val
                    route = ''.join(route_parts)
                    data = {
                        'summary': func.__doc__ or 'Route for {}'.format(route),
                        'parameters': [
                            {
                                'name': name,
                                'in': 'path',
                                'required': True,
                                'description': '{} for route {}'.format(name, route),
                                'schema': {
                                    'type': {
                                        '': 'string',
                                        'string:': 'string',
                                        'int:': 'integer',
                                        'float:': 'number',
                                        'uuid:': 'string',
                                        'path:': 'string'
                                    }[param_type]
                                }
                            }
                            for param_type, name in re.findall(var_pattern, route)
                        ]
                    }
                    paths.setdefault(re.sub(var_pattern, r'{\2}', route), {})[
                        method.lower()] = data
            vals = new_vals
        return json.dumps({
            'swagger': '2.0',
            'info': {
                'title': '{} API'.format(self._get_app().name.split('.')[0].replace('_', ' ').title()),
                'version': '1.0'
            },
            'paths': paths
        }, indent=4, sort_keys=True)

    def _index(self):
        """Returns a page displaying the endpoint documentation"""
        return swagger_page.format(
            title=self._get_app().name,
            description='Documentation for {}'.format(self._get_app().name),
            yaml_url='/endpoints'
        )

    def _register_resource(self, route, func, method):
        """Register a function, wrapping it with REST helpers"""
        cur_handler = self.routes.get((route, method))
        if cur_handler:
            if cur_handler is not func:
                raise ValueError(
                    'Attempting to register a second method "{}" for the route {}'.format(method.__qualname__, route))
            else:
                return
        self.routes[(route, method)] = func

        @wraps(func)
        def wrapper(*args, __f=func, **kwargs):
            name = __f.__qualname__

            try:
                code = 200
                if '.' in name:
                    out = __f(type(name, (object,), {})(), *args, **kwargs)
                else:
                    out = __f(*args, **kwargs)
            except HTTPException as e:
                out, code = {'error': e.name, 'message': e.description}, e.code
            except BaseException as e:
                print(traceback.format_exc())
                out, code = {'error': 'Internal error', 'message': 'Server encountered an error'}, 500
            return json.dumps(out, indent=4) + '\n', code

        self._get_app().add_url_rule(route, func.__qualname__, wrapper, methods=[method])

    def _set_resource(self, path, data: dict):
        """Recursively build routes from nested dictionaries and register them with the app"""
        for key, val in data.items():
            if key in self.METHODS:
                self._register_resource(path, val, key)
            else:
                if not isinstance(val, dict) or not key.startswith('/'):
                    raise RuntimeError(
                        'Expected either rest call (GET, POST, etc.) or route (/something, /<var>, etc.). Found: "{}"'.format(
                            val))
                self._set_resource(path + key, val)

    def _get_app(self) -> Flask:
        """Return the current app object"""
        if has_app_context():
            return flask.current_app
        else:
            return self.app


swagger_page = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="description" content="{description}">

  <link rel='shortcut icon' type='image/x-icon' href='/favicon.ico'>
  <link rel="stylesheet" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css">
</head>

<body>
  <div id='swagger-ui'></div>
  <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({{
      url: "{yaml_url}",
      dom_id: '#swagger-ui'
    }});
  </script>
</body>
</html>
'''
