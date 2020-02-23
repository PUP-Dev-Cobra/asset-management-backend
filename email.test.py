#!/usr/bin/env python3

from internals.mailgun import send_simple_message
from pathlib import Path

send_simple_message(
    subject='Testing HTML',
    text=Path('./email.template.html')
    .read_text()
    .replace("{{name}}", "Username Test")
    .replace("{{url}}", "http://testing.com/blah-blah")
)
