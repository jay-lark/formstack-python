import requests
import os
from forms.rest_adapter import FormsClient

oauth_token = os.environ["OAUTH_TOKEN"]
fs = FormsClient(hostname=os.environ["API_URL"], token=oauth_token)


def test_create_and_get_form():
    form_data = {
        "db": False,
        "label_position": "top",
        "submit_button_title": "Submit Form",
        "use_ssl": True,
        "timezone": "US/Eastern",
        "language": "en",
        "active": True,
        "name": "this is a test form",
        "num_columns": 2,
    }
    form_create = fs.post("form.json", data=form_data)
    form_id = form_create["id"]
    get_form = fs.get(f"form/{form_id}")
    assert form_create["name"] == "this is a test form"
    assert get_form["name"] == "this is a test form"
    assert get_form["created"] == form_create["created"]
    assert get_form["id"] == form_create["id"]
