import json


class FormstackException(Exception):
    pass


class DocsException(Exception):
    pass


def detect_http_error(response):
    if response.status_code == 401:
        return "Unauthorized - Valid OAuth2 credentials were not supplied"
    elif response.status_code == 403:
        return "Forbidden - The current user does not have access to this method"
    elif response.status_code == 404:
        return "Not Found - The resource requested could not be found"
    elif response.status_code == 405:
        return "Method Not Allowed - The requested method does not exist"
    elif response.status_code == 415:
        return "Unsupported Media Type - A valid media type (JSON, XML, HTTP URL encoded) was not used"
    elif response.status_code == 429:
        return "Too Many Requests - The current user has hit the daily rate limit"
    elif response.status_code >= 500:
        return (
            "5xx Internal Server Error - An error occurred while processing the request"
        )

    elif response.status_code >= 400:
        return response.status_code + " server error"
