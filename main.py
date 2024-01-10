from formstack.forms_api import FormsClient
from formstack.docs_api import DocsClient
import os

oauth_token = os.environ["OAUTH_TOKEN"]
scim_token = os.environ["SCIM_TOKEN"]

docs_secret = "WWP9T946"
docs_key = "EE7Y3KZHZXIEZAYITV5PVGJ64Q3R"

fs = FormsClient(token=oauth_token)

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

params = {"folders": "false", "page": 1, "per_page": 1}

update_data = {"submit_button_title": "Push Here"}

doc_data = '{"name": "Test2"}'
doc_delivery = {"type": "webhook", "url": "https://example.com"}
# form_update = fs.update_form(id=1354156, data=form_fields)
# print(form_update)
submissions = []
submissions_detail = {}
get_form = fs.get_form_submissions(id=5587396)
for submission in get_form["submissions"]:
    submissions.append(submission["id"])

for sub in submissions:
    detail = fs.get_submission(sub)
    submissions_detail.update(
        {
            "submission": {
                "name": detail["data"][0]["value"],
                "email": detail["data"][1]["value"],
                "phone": detail["data"][2]["value"],
                "money": detail["data"][3]["value"],
            }
        }
    )
    print(submissions_detail)

print(submissions_detail)

for x in submissions_detail:
    print(submissions_detail[x]["name"])
