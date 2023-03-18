from flask import current_app, request, abort
from flask_login import current_user
from functools import wraps
import time


def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if (getattr(current_user, 'role_id', None) == 3 or
            (request.headers.get('x-api-key') and
             request.headers.get('x-api-key') == current_user.api_key)):
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


def require_public_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if (getattr(current_user, 'role_id', None) == 3 or
            (request.headers.get('x-api-key') and
             (request.headers.get('x-api-key') == current_app.config.get('PUBLIC_API_KEY') or
              request.headers.get('x-api-key') == current_user.api_key))):
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


def format_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return {'result': result, 'exec_time': end - start}
    return wrapper
