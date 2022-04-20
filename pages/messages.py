import json
from flask import request
from wtforms import Form, IntegerField, validators
from pages.communities import QUERY_TYPES
from util import bad_request
from . import common_fields
from . import common_forms

class MessagesArgs(Form):
    start = IntegerField("start", [validators.InputRequired()])
    max = IntegerField("max", [validators.InputRequired()])
    hardware = common_fields.buildHardwareField()
    uid = common_fields.buildUidField()
    language = common_fields.buildLanguageField()
    timezoneOffset = common_fields.buildTimezoneOffsetField()
    qt = common_fields.buildQtField()

class MessagesForm(common_forms.TokenForm):
    def __init__(self, formdata):
        super().__init__(formdata, False)

def messages_read():
    messages = {}
    return "messages:" + json.dumps(messages)

QUERY_TYPES = {
    "messages-read": messages_read
}

def messages_request_dispatch():
    args = MessagesArgs(request.args)
    if not args.validate():
        return bad_request("invalid messages args")

    form = MessagesForm(request.form)
    if not form.validate():
        return bad_request("invalid messages form")

    if not form.tokenValid():
        return bad_request("unauthenticated")

    qt = request.args["qt"]
    if qt in QUERY_TYPES:
        return QUERY_TYPES[qt]()

    return bad_request("unknown qt in messages")
