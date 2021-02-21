from flask import jsonify


def make_error(code_message):
    response = jsonify({
        'status_code': code_message[0],
        'message': code_message[1]
    })
    response.status_code = code_message[0]
    return response


INVALID_JSON_SENT = (400, 'invalid json was sent to the server')
UNAUTHORIZED = (401, 'unauthorized')
FORBIDDEN = (403, 'forbidden')

USER_EXISTS = (429, 'user already exists')
USER_NOT_FOUND = (404, 'user not found')
ERROR_USER_NOT_FOUND = (400, 'user not found')

ROLE_EXISTS = (429, 'role already exists')
ROLE_NOT_FOUND = (404, 'role not found')
ERROR_ROLE_NOT_FOUND = (400, 'role not found')

INVALID_IPV4_SENT = (400, 'invalid ipv4 was sent to the server')
INVALID_DOMAIN_SENT = (400, 'invalid domain was sent to the server')
