import requests
import socket
from flask import jsonify, request

from ioc_fetch.api import api
from ioc_fetch.api.lib.decorators.auth import require_roles
from ioc_fetch.api.lib.responses import *
from ioc_fetch.api.sources import all_sources
from ioc_fetch.lib.util import get_env_variable
from ioc_fetch.logger import get_logger


logger = get_logger(__name__)


@api.route('/ipv4/<ipv4>', methods=['GET'])
@require_roles(roles=['user'])
def get_ipv4(ipv4, **kwargs):
    if not is_valid_ipv4_address(ipv4):
        return make_error(INVALID_IPV4_SENT)

    result = {}
    for source in all_sources:
        try:
            response = source.check_ipv4(ipv4)
            result[source.__class__.__name__.lower()] = response.json()
        except Exception as e:
            logger.exception(e)
    return jsonify(result)


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False
    return True

