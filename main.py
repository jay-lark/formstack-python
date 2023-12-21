from forms.rest_adapter import FormsClient
import os

oauth_token = os.environ["oauth_token"]

#list the forms in your account
fs= FormsClient(token = oauth_token)

form_list = fs.get("form.json")
print(form_list)

#create a form
params = {
    "db": False,
    "label_position": "top",
    "submit_button_title": "Submit Form",
    "use_ssl": False,
    "timezone": "US/Eastern",
    "language": "en",
    "active": False,
    "name": "this is a test form",
    "num_columns": 2
}
form_create = fs.post("form.json", params=params)
