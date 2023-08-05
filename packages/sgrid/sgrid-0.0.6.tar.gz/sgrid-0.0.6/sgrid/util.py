import logging
import time

import requests

logger = logging.getLogger(__name__)


def ping_service(url, retries=10, sleep=1, condition=None):
    for _ in range(retries):
        try:
            resp = requests.get(url)
            if condition is not None:
                if not condition(resp):
                    raise AssertionError
            return True
        except:
            logger.info('Waiting for service %s' % url)
            time.sleep(sleep)
