# Backplate API

Create beautiful Flask-based, RESTful APIs with Backplate's API helper methods.

```bash
$ pip install backplate
```

## Features

- Focus on creating app specific logic instead of API boilerplate.
- Easily define nestable endpoints with endpoint generation helpers.
- JSON mediatype response formatting by default.
- Sleek error handling architecture for validation and exceptions.
- Default data enveloping for data and error responses.
- Seamless integration of authentication flows with [backplate-auth](https://github.com/studioarmix/backplate-auth).

- [Documentation](https://github.com/studioarmix/backplate/tree/master/docs)
- [Example Project App (Source)](https://github.com/studioarmix/backplate/tree/master/example)

## Quickstart

Creating a simple Flask-based API app prefixed with `/v1`.

- Creates endpoints for `me` and `item` under the names `/me` and `/items`
- Endpoints such as `items` can have:
  - indexController (`/items`) and,
  - childController (`/items/:id`).

```python
# example.py

from flask import Flask
from flask_restful import Resource
from backplate import create_api, Route

class Profile(Resource):
    # /v1/me
    def get(self):
        return {'id': 1}

class Items(Resource):
    # /v1/items
    def get(self):
        return [{'id': idx} for idx in range(0, 20)]

class Item(Resource):
    # /v1/items/:id
    def get(self, id):
        return {'id': id}

routes = [
    Route('me', '/me', Profile),
    Route('item', '/items', Items, Item)
]

app = create_api(__name__, routes=routes)

if __name__ == '__main__':
    app.run()

```

### Error Handling
Passing `errors` parameter into `create_api()` enables for a consistent error handling experience.

```python
# example.py

from backplate import APIError, errordef

# ...
# define your error codes

ERR_TEAPOT = 'ERR_TEAPOT'
errors = [
    errordef(ERR_TEAPOT, 418, 'I am a custom error.')
]

# ...
# define your api resources which raise errors

class Item(Resource):
    def get(self, id):
        # raise custom error
        raise APIError(ERR_TEAPOT, data={
            'fields': {'random': 'Incorrect anything.'}})

# ...
# create api with error definitions

app = create_api(..., errors=errors)
```

The `APIError` constructor takes `code`, and optional arguments `status`, and `description`.

The `code` argument is used to match an error created by `errordef()` in the `errors` array (which is converted into a dict/map internally), and then (using the pre-defined `errors` map as a fallback) generates and formats an appropriate error response with HTTP status code.

Raising an error like `raise APIError(ERR_TEAPOT)` will then be formatted and completed to use the fallback `code` and `description` values provided in the `errors` array that was passed to the `create_api()` method.

Errors do not need to be defined in the `errors` array to be raised.




