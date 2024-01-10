Import the library and initialize the client
```
from formstack.forms_api import FormsClient

oauth_token = os.environ["OAUTH_TOKEN"]

fs= FormsClient(token = oauth_token)
```

Get all the forms in your account

```
get_form = fs.get_form()
```

Get a specific form
```
get_form = fs.get_form(id=1234)
```
Get a form's basic details
```
get_form = fs.get_form(id=1234, detail="basic")
```
Get a form's html
```
get_form = fs.get_form(id=1234, detail="html")
```
Pass Parameters into getting a form
```
params = {"folders": "false", "page": 10, "per_page": 10}

get_form = fs.get_form(params=params)

```

Create a form
```
form_data = {
    "db": True,
    "label_position": "top",
    "submit_button_title": "Submit Form",
    "use_ssl": True,
    "timezone": "US/Eastern",
    "language": "en",
    "active": True,
    "name": "This is my test form",
    "num_columns": 2,
    "fields": [
        {"field_type": "text", "label": "test short answer 1"},
        {"field_type": "textarea", "label": "test long answer 1"},
    ],
}

create_form = fs.create_form(data=form_data)
```

Update a form
```
update_data = {"submit_button_title": "Push Here"}
update_form = fs.update_form(id=12345, data=update_data)
```

Delete a form
```
delete_form = fs.delete_form(id=12345)
```