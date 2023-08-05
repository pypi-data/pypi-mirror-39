"""
    !!!MODIFIED BY 15FIVE!!! 
    Modifiers: Andrii Pleskach, Paul Logston

"""
import logging
import requests


logger = logging.getLogger(__name__)


def http_post(endpoint, data):
    """
        :param endpoint:  endpoint URL
        :param data:  The array of JSONs to be sent
        :type  endpoint:  string
        :type  data:  string
    """
    logger.info("Sending POST request to %s..." % endpoint)
    logger.debug("Payload: %s" % data)
    r = requests.post(endpoint, data=data, headers={'content-type': 'application/json; charset=utf-8'})
    getattr(logger, "info" if is_good_status_code(r.status_code) else "warn")(
        "POST request finished with status code: " + str(r.status_code))
    return r


def http_get(endpoint, payload):
    """
        :param endpoint:  endpoint URL
        :param payload:  The event properties
        :type  endpoint:  string
        :type  payload:  dict(string:*)
    """
    logger.info("Sending GET request to %s..." % endpoint)
    logger.debug("Payload: %s" % payload)
    r = requests.get(endpoint, params=payload)
    getattr(logger, "info" if is_good_status_code(r.status_code) else "warn")(
        "GET request finished with status code: " + str(r.status_code))
    return r


def is_good_status_code(status_code):
    """
        :param status_code:  HTTP status code
        :type  status_code:  int
        :rtype:              bool
    """
    return 200 <= status_code < 400
