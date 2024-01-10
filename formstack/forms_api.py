import requests
import requests.packages
from typing import List, Dict
from . import exceptions
from json import JSONDecodeError
from formstack.models import Result
import logging


class FormsClient:
    def __init__(
        self,
        hostname: str = "www.formstack.com",
        token: str = "",
        ver: str = "v2",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self._logger = logger or logging.getLogger(__name__)
        self.url = "https://{}/api/{}/".format(hostname, ver)
        self._token = token
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def get(self, endpoint: str, enc_password: str = "", params: Dict = None):
        return self._do(
            http_method="GET",
            endpoint=endpoint,
            params=params,
            enc_password=enc_password,
        )

    def post(
        self,
        endpoint: str,
        enc_password: str = "",
        params: Dict = None,
        data: Dict = None,
    ):
        return self._do(
            http_method="POST",
            endpoint=endpoint,
            params=params,
            data=data,
            enc_password=enc_password,
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
        enc_password: str = "",
        params: Dict = None,
        data: Dict = None,
    ):
        full_url = self.url + endpoint
        headers = {
            "authorization": "Bearer " + self._token,
            "content-type": "application/json",
            "accept": "application/json",
        }
        if enc_password != "":
            headers["X-FS-ENCRYPTION-PASSWORD"] = enc_password

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
            raise Exception("Reqest failed from e")
        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            # raise Exception("Bad JSON in response") from e
        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = response.status_code
        if is_success:  # OK
            return data_out
        self._logger.error(msg=log_line)
        return exceptions.detect_http_error(response)

    # Forms
    def get_form(
        self,
        params: str = "",
        id: int = "",
        detail: str = "",
    ):
        urlpath = ""
        if id != "":
            urlpath = "/" + str(id) + "/" + detail
        return self.get(
            endpoint=f"form{urlpath}.json",
            params=params,
        )

    def create_form(self, params: Dict = None, data: Dict = None):
        return self.post(endpoint="form.json", params=params, data=data)

    def update_form(self, id: int = "", data: Dict = None):
        return self.put(endpoint=f"form/{id}.json", data=data)

    def delete_form(self, id: int = ""):
        return self.delete(endpoint=f"form/{id}.json")

    # Field
    def get_field(self, id: int = ""):
        return self.get(endpoint=f"field/{id}.json")

    def update_field(self, id: int = "", data: Dict = ""):
        return self.put(endpoint=f"field/{id}.json", data=data)

    def delete_field(self, id: int = ""):
        return self.delete(endpoint=f"field/{id}.json")

    # Form Fields
    def get_form_fields(self, id: int = ""):
        return self.get(endpoint=f"form/{id}/field.json")

    def new_form_field(self, id: int = "", data: Dict = ""):
        return self.post(endpoint=f"form/{id}/field.json", data=data)

    # Folders
    def get_folder(self, id: int = "", params: Dict = None):
        urlpath = ""
        if id != "":
            urlpath = "/" + str(id)
        return self.get(endpoint=f"folder{urlpath}.json", params=params)

    def create_folder(self, params: Dict = None, data: Dict = None):
        return self.post(endpoint="folder.json", params=params, data=data)

    def update_folder(self, params: Dict = None, data: Dict = None):
        return self.put(endpoint="folder.json", params=params, data=data)

    def delete_folder(self, id: int = ""):
        return self.delete(endpoint=f"folder/{id}.json")

    # Submissions
    def get_submission(self, id: int = "", params: Dict = None):
        return self.get(endpoint=f"submission/{id}.json", params=params)

    def update_submission(self, data: Dict = None):
        return self.put(endpoint=f"submission/{id}.json", data=data)

    def delete_submission(self, id: int = ""):
        return self.delete(endpoint=f"submission/{id}.json")

    # Form Submissions
    def get_form_submissions(
        self, id: int = "", params: Dict = None, enc_password: str = ""
    ):
        return self.get(
            endpoint=f"form/{id}/submission.json",
            params=params,
            enc_password=enc_password,
        )

    def create_form_submission(self, id: int = "", data: Dict = ""):
        return self.post(endpoint=f"form/{id}/submission.json", data=data)

    # Download
    def download_form_submission(self, id: int, field_id: int):
        return self.post(endpoint=f"download/{id}/{field_id}.json")

    # Partial Submissions
    def get_form_partial_submissions(self, id: int = "", params: Dict = None):
        return self.get(endpoint=f"form/{id}/partialsubmission.json", params=params)

    def get_partial_submission(self, id: int, params: Dict = None):
        return self.get(endpoint=f"partialsubmission/{id}.json", params=params)

    def delete_submission(self, id):
        return self.delete(endpoint=f"partialsubmission/{id}.json")

    # Confirmation
    def create_confirmation_email(self, id, data: Dict = None):
        return self.delete(endpoint=f"form/{id}/confirmation.json", data=data)

    def get_confirmation(self, id: int):
        return self.get(endpoint=f"confirmation/{id}.json")

    def update_confirmation(self, id: int, data: Dict = None):
        return self.put(endpoint=f"confirmation/{id}.json", data=data)

    def delete_confirmation(self, id: int):
        return self.delete(endpoint=f"confirmation/{id}.json")

    # Notifications
    def create_notification_email(self, id, data: Dict = None):
        return self.delete(endpoint=f"form/{id}/notification.json", data=data)

    def get_notification(self, id: int):
        return self.get(endpoint=f"notification/{id}.json")

    def update_notification(self, id: int, data: Dict = None):
        return self.put(endpoint=f"notification/{id}.json", data=data)

    def delete_notification(self, id: int):
        return self.delete(endpoint=f"notification/{id}.json")

    # Webhooks
    def create_webhook(self, id, data: Dict = None):
        return self.delete(endpoint=f"form/{id}/webhook.json", data=data)

    def get_webhook(self, id: int):
        return self.get(endpoint=f"webhook/{id}.json")

    def update_webhook(self, id: int, data: Dict = None):
        return self.put(endpoint=f"webhook/{id}.json", data=data)

    def delete_webhook(self, id: int):
        return self.delete(endpoint=f"webhook/{id}.json")

    # Portals
    def get_portal(
        self,
        id: int = "",
    ):
        urlpath = ""
        if id != "":
            urlpath = "/" + str(id)
        return self.get(endpoint=f"portal{urlpath}")

    def update_portal(self, id: int, data: Dict = None):
        return self.get(endpoint=f"portal/{id}", data=data)

    def delete_portal(self, id: int):
        return self.get(endpoint=f"portal/{id}")

    def create_portal_copy(self, id: int):
        return self.post(endpoint=f"portal/{id}/copy")

    def create_portal_avatar(self, id: int, data: Dict = None):
        return self.post(endpoint=f"portal/{id}/avatar", data=data)

    def delete_portal_avatar(self, id: int):
        return self.post(endpoint=f"portal/{id}/avatar")

    def create_portal_user(self, id: int, data: Dict = None):
        return self.post(endpoint=f"portal/{id}/user", data=data)

    def update_portal_user(self, id: int, data: Dict = None):
        return self.put(endpoint=f"portal/{id}/user", data=data)

    def delete_portal_user(self, id: int):
        return self.delete(endpoint=f"portal/{id}/user")

    def add_portal_form(self, id: int, data: Dict = None):
        return self.delete(endpoint=f"portal/{id}/form", data=data)

    def update_portal_form(self, id: int, form_id: int, data: Dict = None):
        return self.put(endpoint=f"portal/{id}/form/{form_id}", data=data)

    def delete_portal_form(self, id: int, form_id: int):
        return self.delete(endpoint=f"portal/{id}/form/{form_id}")

    # Smartlists
    def get_smartlists(self, params: Dict = None):
        return self.get(endpoint="smartlist", params=params)

    def get_smartlist(self, id: int):
        return self.get(endpoint=f"smartlist/{id}")

    def create_smartlist(self, data: Dict = None):
        return self.get(endpoint=f"smartlist", data=data)

    def update_smartlist(self, id: int, data: Dict = None):
        return self.get(endpoint=f"smartlist/{id}", data=data)

    def delete_smartlist(self, id: int):
        return self.get(endpoint=f"smartlist/{id}")

    def get_smartlist_options(self, id: int, params: Dict = None):
        return self.get(endpoint=f"smartlist/{id}/option", params=params)

    def update_smartlist_options(self, id: int, data: Dict = None):
        return self.put(endpoint=f"smartlist/{id}/option", data=data)

    def get_smartlist_option(self, id: int, option_id: int):
        return self.get(endpoint=f"smartlist/{id}/option{option_id}")

    def update_smartlist_option(self, id: int, option_id: int, data: Dict = None):
        return self.put(endpoint=f"smartlist/{id}/option{option_id}", data=data)

    def delete_smartlist_option(self, id: int, option_id: int):
        return self.delete(endpoint=f"smartlist/{id}/option{option_id}")

    def update_smartlist_option_image(self, id: int, option_id: int):
        return self.put(endpoint=f"smartlist/{id}/option{option_id}")

    def delete_smartlist_option_image(self, id: int, option_id: int, data: Dict = None):
        return self.delete(endpoint=f"smartlist/{id}/option{option_id}", data=data)

    def delete_smartlist_options(self, id: int):
        return self.put(endpoint=f"smartlist/{id}/alloptions")

    def update_smartlist_options_bulk(self, id: int, data: Dict = None):
        return self.put(endpoint=f"smartlist/{id}/bulkoptions", data=data)
