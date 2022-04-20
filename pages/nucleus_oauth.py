import json
from flask import request
from wtforms import Form, StringField, IntegerField, validators
from pages.communities import QUERY_TYPES
from util import bad_request
import config
from . import common_fields

class NucleusOAuthArgs(Form):
    type = StringField("type", [validators.AnyOf("server_token")])
    code = StringField("code", [validators.Length(35, 45)])
    forceTrial = IntegerField("forceTrial", [validators.InputRequired(), validators.NumberRange(0, 1)])
    proto = IntegerField("proto", [validators.InputRequired()])
    json = IntegerField("json", [validators.InputRequired(), validators.NumberRange(0, 1)])
    env = common_fields.buildEnvField()
    userId = StringField("userId", [validators.Regexp("[0-9a-f]+")]) # uid in hex
    qt = common_fields.buildQtField()

class NucleusOAuthForm(Form):
    entitlements = StringField("entitlements", [validators.Length(1, 4096)])

def nucleusOAuth_origin_requesttoken():
    if request.args.get("type", None) == "server_token":
        result = {
            "token": config.MOCK_NUCLEUS_TOKEN,
            "hasOnlineAccess": "1",
            "expiry": "14399",
            "storeUri": "https://www.origin.com/store/titanfall/titanfall-2/standard-edition"
        }
        return json.dumps(result)
    return bad_request("unsupport origin request type")

QUERY_TYPES = {
    "origin-requesttoken": nucleusOAuth_origin_requesttoken
}

def nucleusOAuth_request_dispatch():
    args = NucleusOAuthArgs(request.args)
    if not args.validate():
        return bad_request("invalid n-oauth args")

    form = NucleusOAuthForm(request.form)
    if not form.validate():
        return bad_request("invalid n-oauth form")

    qt = request.args["qt"]
    if qt in QUERY_TYPES:
        return QUERY_TYPES[qt]()

    return bad_request("unsupported n-oauth qt")
