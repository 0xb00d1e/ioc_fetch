import requests
import socket
from flask import jsonify, request

from ioc_fetch.api import api
from ioc_fetch.api.lib.decorators.auth import require_roles
from ioc_fetch.api.lib.responses import *
from ioc_fetch.api.sources import all_sources
from ioc_fetch.logger import get_logger


logger = get_logger(__name__)


@api.route('/domain/<domain>', methods=['GET'])
@require_roles(roles=['user'])
def get_domain(domain, **kwargs):
    if not is_valid_domain(domain):
        return make_error(INVALID_DOMAIN_SENT)

    result = {}
    for source in all_sources:
        try:
            response = source.check_domain(domain)
            result[source.__class__.__name__.lower()] = response.json()
        except NotImplementedError:
            continue
        except Exception as e:
            logger.exception(e)
    return jsonify(result)


def is_valid_domain(domain):
    # TODO  Add better validation
    # Distinguish between domain and ipv4
    if '.' not in domain:
        return False
    return True
