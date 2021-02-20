from functools import wraps

from flask import request

from ioc_fetch.api.lib.responses import *
from ioc_fetch.api.models.user import User


def require_roles(roles=[]):
    def require_roles_decorator(view_function):
        @wraps(view_function)
        def _require_roles(*args, **kwargs):
            key = request.args.get('key', '')
            if not key:
                key = request.headers.get('X-API-Key', '')

            if key:
                user = User.get_user_by_apikey(key)
                if not user:
                    return make_error(UNAUTHORIZED)
                if not user.is_active:
                    return make_error(FORBIDDEN)
                if user:
                    kwargs['username'] = user.username
                    if set(roles) <= set(user.role_names()):
                        return view_function(*args, **kwargs)
                    else:
                        return make_error(FORBIDDEN)
                else:
                    return make_error(UNAUTHORIZED)
            else:
                return make_error(UNAUTHORIZED)

            return view_function(*args, **kwargs)
        return _require_roles
    return require_roles_decorator
