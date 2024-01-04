# formstack-python

Python Wrapper for Formstack API

Include this repository in your project and then list all your forms like this

```
from forms.rest_adapter import FormsClient
import os

oauth_token = os.environ["oauth_token"]

fs= FormsClient(token = oauth_token)

form_list = fs.get_form()
print(form_list)

#get details for specific form
form_details = fs.get_form(id = 1234)
print(form_details)
```

or create a form

```
from forms.rest_adapter import FormsClient
import os

oauth_token = os.environ["oauth_token"]

form_fields= {
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
form_create = fs.create_form(data=form_fields)

```
