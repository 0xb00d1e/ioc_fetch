import re
from flask import jsonify, request

from ioc_fetch.api import api
from ioc_fetch.api.lib.decorators.auth import require_roles
from ioc_fetch.api.lib.responses import *
from ioc_fetch.api.sources import all_sources
from ioc_fetch.logger import get_logger


logger = get_logger(__name__)


@api.route('/sha1/<sha1>', methods=['GET'])
@require_roles(roles=['user'])
def get_sha1(sha1, **kwargs):
    if not is_valid_sha1(sha1):
        return make_error(INVALID_SHA1_SENT)

    result = {}
    for source in all_sources:
        try:
            response = source.check_sha1(sha1)
            result[source.__class__.__name__.lower()] = response.json()
        except NotImplementedError:
            continue
        except Exception as e:
            logger.exception(e)
    return jsonify(result)


def is_valid_sha1(sha1):
    return re.match(r'[0-9a-f]{40}$', sha1, re.I)
