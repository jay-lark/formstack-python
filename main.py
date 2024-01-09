from formstack.forms_api import FormsClient
import os

oauth_token = os.environ["OAUTH_TOKEN"]

fs = FormsClient(hostname="www.formstack.com", token=oauth_token)

form_fields = {
    "db": True,
    "use_ssl": True,
    "active": True,
    "submit_button_title": "give me",
}
# form_update = fs.update_form(id=1354156, data=form_fields)
# print(form_update)

get_form = fs.get_smartlists()
print(get_form)
