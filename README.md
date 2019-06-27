# Flask Resto

*RESTful APIs with Flask for lazy people*

Features Resto gives you:

 - Nice REST integration with Flask
    - Auto-serialize JSON: `return {'val': 12}` -> "`{"val": 12}`"
    - Return proper http/JSON errors on Werkzeug exceptions: `raise Unauthorized` -> `{"error": "Unauthorized", "message": "...`
 - Automatically raise `BadRequest` when an attribute in the json is missing: `api.json['mykey']`
 - Automatically raise `Unauthorized` when a certain auth header is missing: `api.auth['token']`
 - Automatically raise `BadRequest` when a parameter in the URL is missing: `api.params['myparam']`
 - Automatically generate and serve swagger documentation at root URL
 - Group functions however you want in classes and assign them to any route later:

```
class User:
	def create(self):
		...
	
	def get(self, uuid):
		...
	
	def update(self, uuid):
		...
	
	def signup(self):
		...
	
	def login(self):
		...
	
	def refresh_auth(self):
		...


api.resources = {
    '/v1': {
        '/user': {
            'POST': User.create,
        	'/<user_uuid>': {
        		'GET': User.get,
				'PATCH': User.update
			}
        },
        '/auth': {
            '/signup': {'POST': User.signup},
            '/login': {'POST': User.login},
            '/refresh': {'POST': User.refresh}
        }
    }
}
```

## Installation

```bash
pip install flask-resto
```

