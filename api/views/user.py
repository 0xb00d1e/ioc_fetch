import json

import sqlalchemy
from flask import jsonify, request

from ioc_fetch.api import api
from ioc_fetch.api.lib.decorators.auth import require_roles
from ioc_fetch.api.lib.responses import *
from ioc_fetch.api.models import Role, User
from ioc_fetch.app import db


@api.route('/user/<user_id>', methods=['GET'])
@require_roles(roles=['admin'])
def get_user(user_id, **kwargs):
    user = User.get_by_id(user_id)
    if not user:
        return make_error(USER_NOT_FOUND)
    return user.json()


@api.route('/user/', methods=['POST'])
@require_roles(roles=['admin'])
def create_user(**kwargs):
    try:
        data = json.loads(request.data)
    except JSONDecodeError as e:
        make_error(INVALID_JSON_SENT)

    try:
        user = User.create(
            data['username'],
            data['password'],
            data['role_names']
        )
    except sqlalchemy.exc.IntegrityError as e:
        return make_error(USER_EXISTS)
    except KeyError as e:
        return make_error((400, '%s key missing' % e))
    except ValueError as e:
        return make_error((400, str(e)))
    return jsonify(user.json())


@api.route('/user/<user_id>', methods=['PATCH'])
@require_roles(roles=['admin'])
def edit_user(user_id, **kwargs):
    user = User.get_by_id(user_id)
    if not user:
        return make_error(USER_NOT_FOUND)

    try:
        data = json.loads(request.data)
    except JSONDecodeError as e:
        return make_error(INVALID_JSON_SENT)

    for key, value in data.items():
        if key == 'role_names':
            for role in value:
                r = Role.get_by_name(role)
                if not r:
                    return make_error(ROLE_NOT_FOUND)
                user.roles.append(r)
        setattr(user, key, value)
    db.session.commit()
    return user.json()


@api.route('/user/<user_id>', methods=['DELETE'])
@require_roles(roles=['admin'])
def delete_user(user_id, **kwargs):
    user = User.get_by_id(user_id)
    if not user:
        return make_error(USER_NOT_FOUND)

    db.session.delete(user)
    db.session.commit()
    return user.json()
