import json

import sqlalchemy
from flask import jsonify, request

from ioc_fetch.api import api
from ioc_fetch.api.lib.decorators.auth import require_roles
from ioc_fetch.api.lib.responses import *
from ioc_fetch.api.models import Role
from ioc_fetch.app import db


@api.route('/role/<role_id>', methods=['GET'])
@require_roles(roles=['admin'])
def get_role(role_id, **kwargs):
    role = Role.get_by_id(role_id)
    if not role:
        return make_error(ROLE_NOT_FOUND)
    return role.json()


@api.route('/role/', methods=['POST'])
@require_roles(roles=['admin'])
def create_role(**kwargs):
    try:
        data = json.loads(request.data)
    except JSONDecodeError as e:
        make_error(INVALID_JSON_SENT)

    try:
        role = Role.create(
            data['name']
        )
    except sqlalchemy.exc.IntegrityError as e:
        return make_error(ROLE_EXISTS)
    except KeyError as e:
        return make_error((400, '%s key missing' % e))
    except ValueError as e:
        return make_error((400, str(e)))
    return jsonify(role.json())


@api.route('/role/<role_id>', methods=['PATCH'])
@require_roles(roles=['admin'])
def edit_role(role_id, **kwargs):
    role = Role.get_by_id(role_id)
    if not role:
        return make_error(ROLE_NOT_FOUND)

    try:
        data = json.loads(request.data)
    except JSONDecodeError as e:
        return make_error(INVALID_JSON_SENT)

    for key, value in data.items():
        setattr(role, key, value)
    db.session.commit()
    return role.json()


@api.route('/role/<role_id>', methods=['DELETE'])
@require_roles(roles=['admin'])
def delete_role(role_id, **kwargs):
    role = Role.get_by_id(role_id)
    if not role:
        return make_error(ROLE_NOT_FOUND)

    db.session.delete(role)
    db.session.commit()
    return role.json()
