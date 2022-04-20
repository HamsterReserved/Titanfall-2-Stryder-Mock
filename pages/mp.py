from flask import request
from wtforms import Form, IntegerField, validators
from util import bad_request
import config
from . import common_fields
from . import common_forms

class MpArgs(Form):
    hardware = common_fields.buildHardwareField()
    uid = common_fields.buildUidField()
    wait = IntegerField("wait", [validators.InputRequired()]) # waited seconds at main screen
    prot = IntegerField("prot", [validators.InputRequired()])

class MpForm(common_forms.TokenForm):
    language = common_fields.buildLanguageField()
    dc = common_fields.buildDCField()
    isTrial = common_fields.buildIsTrialField()
    ver = common_fields.buildVerField()
    EAAccess = common_fields.buildEAAccessField()

    def __init__(self, formdata):
        super().__init__(formdata, allow_empty=True)

    def mpValidForm(self):
        if self["NucleusToken"].data == config.MOCK_NUCLEUS_TOKEN:
            return True
        return False

def mp_request_dispatch():
    args = MpArgs(request.args)
    if not args.validate():
        return bad_request("invalid mp args")

    form = MpForm(request.form)
    if not form.validate():
        return bad_request("invalid mp form")

    if form.mpValidForm():
        return f"""
convars: {{ stryder_security: "{config.MOCK_STRYDER_SECURITY}" }}
concommands:
[ "getNewAuthToken" ]
convars: {{ rspn_motd: "Titanfall is the very core of Respawn's DNA.", mp_allowed: "1"   }}
        """

    return 'convars: { mp_permission_requestInterval: "1" }'
