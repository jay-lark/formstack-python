import requests
import requests.packages
from typing import List, Dict
from formstack.exceptions import FormstackException
from json import JSONDecodeError
from formstack.models import Result
import logging


class FormsSCIM:
    def __init__(
        self,
        hostname: str = "www.formstack.com",
        token: str = "",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self._logger = logger or logging.getLogger(__name__)
        self.url = "https://{}/scim/".format(hostname)
        self._token = token
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def get(self, endpoint: str, params: Dict = None):
        return self._do(
            http_method="GET",
            endpoint=endpoint,
            params=params,
        )

    def post(
        self,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
    ):
        return self._do(
            http_method="POST",
            endpoint=endpoint,
            params=params,
            data=data,
        )

    def put(self, endpoint: str, params: Dict = None, data: Dict = None):
        return self._do(
            http_method="PUT",
            endpoint=endpoint,
            params=params,
            data=data,
        )

    def delete(self, endpoint: str, params: Dict = None, data: Dict = None):
        return self._do(
            http_method="DELETE",
            endpoint=endpoint,
            params=params,
            data=data,
        )

    def _do(
        self,
        http_method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
    ):
        full_url = self.url + endpoint
        headers = {
            "authorization": "Bearer " + self._token,
            "content-type": "application/json",
            "accept": "application/json",
        }

        log_line_pre = f"method={http_method}, url={full_url}, params={params}"
        log_line_post = ", ".join(
            (log_line_pre, "success={}, status_code={}, message={}")
        )
        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(
                method=http_method,
                url=full_url,
                verify=self._ssl_verify,
                headers=headers,
                params=params,
                json=data,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise FormstackException("Reqest failed from e")
        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise FormstackException("Bad JSON in response") from e
        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = log_line_post.format(
            is_success, response.status_code, response.reason
        )
        if is_success:  # OK
            self._logger.debug(msg=log_line)
            return data_out
        self._logger.error(msg=log_line)
        raise Exception(f"{response.status_code}: {response.reason}")

    # Users
    def get_users(self, params: Dict = None):
        return self.get(endpoint=f"Users", params=params)

    def create_users(self, data: Dict = None):
        return self.get(endpoint=f"Users", data=data)

    def get_user(self, id: int):
        return self.get(endpoint=f"Users/{id}")

    def update_user(self, id: int, data: Dict = None):
        return self.get(endpoint=f"Users/{id}", data=data)

    def delete_user(self, id: int):
        return self.delete(endpoint=f"Users/{id}")

    # Groups
    def get_groups(self, params: Dict = None):
        return self.get(endpoint=f"Groups", params=params)

    def create_groups(self, data: Dict = None):
        return self.get(endpoint=f"Groups", data=data)

    def get_group(self, id: int):
        return self.get(endpoint=f"Groups/{id}")

    def update_group(self, id: int, data: Dict = None):
        return self.get(endpoint=f"Groups/{id}", data=data)

    def delete_group(self, id: int):
        return self.delete(endpoint=f"Groups/{id}")

    # Forms
    def get_forms(self, params: Dict = None):
        return self.get(endpoint=f"Forms", params=params)

    def get_form(self, id: int):
        return self.get(endpoint=f"Forms{id}")

    # Folders
    def get_folders(self, params: Dict = None):
        return self.get(endpoint=f"Folders", params=params)

    def get_folder(self, id: int):
        return self.get(endpoint=f"Folders{id}")
