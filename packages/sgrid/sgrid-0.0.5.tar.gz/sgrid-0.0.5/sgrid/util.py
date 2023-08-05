import logging
import time

import requests

logger = logging.getLogger(__name__)


def ping_service(url, retries=10, sleep=1):
    for _ in range(retries):
        try:
            requests.get(url)
            return True
        except (ConnectionRefusedError, requests.exceptions.ConnectionError):
            logger.info('Waiting for service %s' % url)
            time.sleep(sleep)
