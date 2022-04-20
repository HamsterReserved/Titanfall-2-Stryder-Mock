from flask import request
from wtforms import Form, StringField, IntegerField, DecimalField, validators
import config
from util import bad_request
from . import common_fields

class EmptyServersArgs(Form):
    dc = common_fields.buildDCField()
    it = IntegerField("it", [validators.InputRequired()])
    searchT = DecimalField("searchT", [validators.InputRequired()])
    qt = common_fields.buildQtField()

class EmptyServerForm(Form):
    vmt = IntegerField("vmt", [validators.NumberRange(1, 1)])
    cdll = IntegerField("cdll", [validators.NumberRange(4294967295, 4294967295)])
    prot = IntegerField("prot", [validators.InputRequired()])
    build = StringField("build", [validators.InputRequired()]) # Titanfall2_v2_0_11_0
    filter = StringField("filter", []) # can be empty
    pVer = IntegerField("pVer", [validators.InputRequired()])
    pVNum = IntegerField("pVNum", [validators.InputRequired()])
    securityToken = common_fields.buildSecurityTokenField()
    securityUID = IntegerField("securityUID", [validators.InputRequired()])
    # unbound dcp0, dcp1... follows

    def tokenValid(self):
        return self["securityToken"].data == config.MOCK_STRYDER_SECURITY

def emptyservers_client():
    return f"""
Servers
{{
	server
	{{
		ip "[::ffff:{config.LOBBY_SERVER_IP}]:0"
		port {config.LOBBY_SERVER_PORT}
		s2sPort {config.LOBBY_SERVER_S2S_PORT}
		key {config.LOBBY_SERVER_KEY}
		sID 0
		np 0
	}}
}}
    """

QUERY_TYPES = {
    "emptyservers-client": emptyservers_client,
}

def emptyservers_request_dispatch():
    args = EmptyServersArgs(request.args)
    if not args.validate():
        return bad_request("invalid mp args")

    form = EmptyServerForm(request.form)
    if not form.validate():
        return bad_request("invalid mp form")

    if not form.tokenValid():
        return bad_request("unauthenticated")

    qt = request.args["qt"]
    if qt in QUERY_TYPES:
        return QUERY_TYPES[qt]()

    return bad_request("unknown qt in emptyservers")
