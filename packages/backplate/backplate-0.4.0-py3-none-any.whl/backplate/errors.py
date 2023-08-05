import re
import logging
import traceback

from flask import jsonify, current_app
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException, InternalServerError, _aborter

log = logging.getLogger(__name__)


class BackplateError(Exception):
    _exceptions = {}

    code = 400
    type = 'GENERAL_EXCEPTION'
    message = 'Application request failed.'

    def __init__(self, type, data=None):
        exception = self._exceptions.get(type)
        if not exception:
            raise ValueError(
                f'{type} is not assigned with {type(self).__name__}.')

        self.type = type
        self.code = exception[0]
        self.message = exception[1]
        super().__init__(self.message)
        self.data = data

    @classmethod
    def assign(cls, exceptions):
        for key, value in exceptions.items():
            if type(value) is not tuple:
                raise ValueError(
                    f"{key} definition '{value}' is not a tuple.")
            if len(value) != 2:
                raise ValueError(
                    f"{key} definition requires tuple of (code, message,)")
        cls._exceptions = exceptions


class Error(object):
    def __init__(self, exception, code=400, typename=None):
        self.exception = exception
        self.code = code
        self.typename = typename


def fmttype(string):
    return string.replace(' ', '_').upper()


def fmtmessage(string):
    return re.sub(r'\s{2,}', ' ', string)


def fmtstackline(line):
    line = re.sub(r'(\n\s*)$', '', line)
    line = re.sub(r'(\n\s*)', ' => ', line)
    line = line.strip().replace('"', "'")
    return line


def fmtstack(stack):
    return [fmtstackline(line) for line in stack]


def create_error_handler(errors=[], json_formatter=None):

    exception_code_map = {}

    for error in errors:
        exception_code_map[error.exception] = {
            'code': error.code,
            'type': fmttype(error.typename) if error.typename else None,
        }

    def handle_error(e):
        error_class = type(e)

        error_code = 500
        error_type = fmttype(HTTP_STATUS_CODES.get(500))
        error_message = fmtmessage(InternalServerError.description),
        error_data = None

        # format http exceptions
        if issubclass(error_class, HTTPException):
            error_code = e.code
            error_type = fmttype(e.name)
            error_message = fmtmessage(e.description)

            _data = getattr(e, 'data', None)
            error_data = (
                _data.get('messages', None)
                if type(_data) is dict else None)

        elif issubclass(error_class, BackplateError):
            error_code = e.code
            error_type = e.type
            error_message = str(e)
            error_data = e.data

        # then userland exceptions
        elif error_class in exception_code_map:
            exception_mapping = exception_code_map[error_class]
            error_code = exception_mapping.get('code')
            error_type = exception_mapping.get('type') or 'REQUEST_ERROR'

            args = e.args[0] if len(e.args) else []
            args = (args,) if type(args) is not tuple else args

            if type(args) is str:
                error_data = args
            # one arg, just error data
            elif len(args) == 1:
                error_data = args[0]
            # two args, error typedef and then data
            elif len(args) == 2:
                # allocate error data from second arg
                error_data = args[1]
                # allocate type from first arg
                error_type = args[0]
                # if it's a tuple it could describe both type and code
                if type(error_type) is tuple:
                    # one arg, just type
                    if len(error_type) == 1:
                        error_type = error_type[0]
                    # two args, type and then code override
                    elif len(error_type) == 2:
                        error_code = error_type[1]
                        error_type = error_type[0]
                    else:
                        raise ValueError(
                            'expecting error typedef with max 2 values')

            if error_code in _aborter.mapping:
                error_message = fmtmessage(
                    _aborter.mapping[error_code].description)

        # everything uncaught
        else:
            DEBUG = current_app.config.get('DEBUG')
            if DEBUG:
                error_data = {
                    'message': str(e),
                    'stack': fmtstack(traceback.format_list(
                        traceback.extract_tb(e.__traceback__))),
                }

        if error_code >= 500:
            log.exception(e)

        error = {
            'code': error_code,
            'type': error_type,
            'message': error_message,
            'data': error_data,
        }

        if callable(json_formatter):
            error = json_formatter(error, error_code)

        return jsonify(error), error_code

    return handle_error


__all__ = [
    'Error',
]
