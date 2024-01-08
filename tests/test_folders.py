import requests
import os
from forms.rest_adapter import FormsClient
import time


oauth_token = os.environ["OAUTH_TOKEN"]
fs = FormsClient(hostname=os.environ["API_URL"], token=oauth_token)


def test_create_get_delete_folder():
    folder_name = str(time.time())
    folder_data = {
        "parent": 0,
        "name": folder_name
    }
    folder_create = fs.create_folder(data=folder_data)
    folder_id = folder_create["id"]
    get_folder = fs.get_folder(id = folder_id)
    assert folder_create["name"] == folder_name
    assert get_folder["name"] == folder_name
    assert get_folder["id"] == folder_create["id"]
    folder_delete = fs.delete_folder(id = folder_id)
    assert folder_delete["id"] == folder_create["id"]
    assert folder_delete["success"] == 1
