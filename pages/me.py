from wtforms import StringField, IntegerField, validators
from flask import request
import config

from util import bad_request
from . import common_fields
from . import common_forms

# me.php does not have args other than qt

class MeForm(common_forms.TokenForm):
    ver = common_fields.buildVerField()
    timezoneOffset = common_fields.buildTimezoneOffsetField()
    hardware = common_fields.buildHardwareField()
    uid = common_fields.buildUidField()
    name = StringField("name", [validators.Length(1, 128)])
    currentRoom = StringField("currentRoom", []) # may be missing
    language = common_fields.buildLanguageField()
    dc = common_fields.buildDCField()
    cprot = IntegerField("cprot", [validators.InputRequired()])
    rep = IntegerField("rep", [validators.InputRequired(), validators.NumberRange(0, 1)])
    ugc = IntegerField("ugc", [validators.InputRequired(), validators.NumberRange(0, 1)])
    isTrial = common_fields.buildIsTrialField()
    EAAccess = common_fields.buildEAAccessField()

    def __init__(self, formdata):
        super().__init__(formdata, False)


def me_request_dispatch():
    if request.args.get("qt", None) != "me":
        return bad_request("invalid me args")

    form = MeForm(request.form)
    if not form.validate():
        return bad_request("invalid me form")

    if not form.tokenValid():
        return bad_request("unauthenticated")

    return f'''
// Current community is 1
// PC-1000674785018, chatroomProt 7, ver 51
// auth is for 1, level member
"chatserverauth": "WJG35yQKEO4L1OHMSvjKBgXQV3Y+D4/GwXdmbWzVxB7fmQHlymwav8dx6XElo/7F",
communities:
{{
	"partial": 1,
	"The Rick Network": 
	{{
		"id": 1,
		"clantag": "ADV",
		"host": "1.1.1.1",
		"port": 27017,
		"room": "c_1_1",
		"pop": 27,
		"nextHappyHour": 58796,
		"nextHappyHourEnd": 62396,
		"happyHour": 0,
		"open": "open",
		"invitesAllowed": 1,
		"chatAllowed": 0,
		"motd": "I am Rick Astley. I will never gonna give you up.",
		"verified": 1,
		"xpRate": 1.0
	}},
}}
currentCommunity: 1
communityMembership: "member"
"pendingRequestCount": 0
currentFaction: "sarah"
"happyHourTimeLeft": 1
inboxstats:
{{
	"latestnoteNum": -1
	"lastReadnoteNum": -1
	"latestmsgNum": -1
	"lastReadmsgNum": -1
	"latesteventNum": -1
	"lastReadeventNum": -1
}}
convars: 
{{
	subscription_hostname: "{config.SUBSCRIPTION_SERVER_IP}"
}}
motd: "I am Rick Astley. I will never gonna give you up."
curtime: 1639928404
region: "Asia"
'''
