import requests
from flask import current_app


def send_simple_message(text, subject="Mail Gun Testing"):
    app = current_app
    return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % (app.config['MAILGUN_DOMAIN']),
        auth=("api", app.config['MAILGUN_API_KEY']),
        data={"from": "Mail Gun Test <mailgun@test.com>",
              "to": app.config['BASE_EMAIL'],
              "subject": subject,
              "html": text}
    )
