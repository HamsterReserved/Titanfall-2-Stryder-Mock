# Handles communities.php requests

import json
from flask import request
from wtforms import Form, validators, IntegerField
from util import bad_request
from . import common_forms
from . import common_fields

# Common fields among communities.php APIs.
# Does not include qt, because it's verified before validation.
class CommunitiesBaseForm(Form):
    hardware = common_fields.buildHardwareField()
    uid = common_fields.buildUidField()
    timezoneOffset = common_fields.buildTimezoneOffsetField()
    language = common_fields.buildLanguageField()

###################### communities-mainmenupromos ###########################

# URL argument validation
# I know it's not a form, but it works anyways.
class CommunitiesMainMenuPromoArgs(CommunitiesBaseForm):
    mainMenuPromos = IntegerField("mainMenuPromos", [validators.NumberRange(1,1)])
    ver = common_fields.buildVerField()
    isTrial = common_fields.buildIsTrialField()
    qt = common_fields.buildQtField()

# Post data validation
class CommunitiesMainMenuPromoForm(common_forms.TokenForm):
    def __init__(self, formdata):
        super().__init__(formdata, allow_empty=True)

def communities_mainmenupromos():
    args = CommunitiesMainMenuPromoArgs(request.args)
    if not args.validate():
        return bad_request("invalid mainmenupromo args")

    form = CommunitiesMainMenuPromoForm(request.form)
    if not form.validate():
        return bad_request("invalid mainmenupromo form")

    promos = {
        "version": 53,
        "newInfo_ImageIndex": 1,
        "largeButton_ImageIndex": 11,
        "smallButton1_ImageIndex": 1,
        "smallButton2_ImageIndex": 12,
        "newInfo_Title1": r"%$rui\/bullet_point%Hamster's Mock Server 1",
        "newInfo_Title2": r"%$rui\/bullet_point%Hamster's Mock Server 2",
        "newInfo_Title3": r"%$rui\/bullet_point%Hamster's Mock Server 3",
        "largeButton_Title": "Frontier News Network: Never Gonna Give You Up",
        "largeButton_Url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "largeButton_Text": "Learn all about what's in this patch available now.",
        "smallButton1_Title": "Rendy Gaming fires away in this Kraber G100 Montage.",
        "smallButton1_Url": "https://www.youtube.com/embed/j7niWUth9_Y?autoplay=1",
        "smallButton2_Title": "Check out the latest weapon skins",
        "smallButton2_Url": "menu:new"
    }
    return "mainMenuPromos: " + json.dumps(promos)

###################### communities-getsettings ###########################

class CommunitiesGetSettingsArgs(CommunitiesBaseForm):
    getsettings = IntegerField("getsettings", [validators.NumberRange(1,1)])
    id = IntegerField("id", [validators.InputRequired()])
    cprot = IntegerField("cprot", [validators.InputRequired()])

class CommunitiesGetSettingsForm(common_forms.TokenForm):
    def __init__(self, formdata):
        super().__init__(formdata, allow_empty=False)

def communities_getsettings():
    args = CommunitiesGetSettingsArgs(request.args)
    if not args.validate():
        return bad_request("invalid getsettings args")

    # TODO: sometimes the game does not send securityToken?
    form = CommunitiesGetSettingsForm(request.form)
    if not form.validate():
        return bad_request("invalid getsettings form")

    settings = {
        "id": 1,
        "name": "The Rick Network",
        "clantag": "RICK",
        "motd": "I am Rick Astley. I will never gonna let you down.",
        "category": "tech",
        "type": "social",
        "visibility": "public",
        "open": "open",
        "mics": "nopref",
        "regions": "North America,Europe,South America,Asia,Oceania",
        "languages": "English,French,German,Italian,Spanish,MSpanish,Japanese,TChinese,Russian,Portuguese,Polish",
        "creatorHardware": "PC",
        "utcHappyHourStart": 8,
        "happyHourStart": 16,
        "invitesAllowed": 0,
        "chatAllowed": 0,
        "creatorUID": 114514,
        "creatorName": "",
        "verified": 1,
        "kills": 1096056980,
        "wins": 77373797,
        "xp": 791295678,
        "deaths": 0,
        "losses": 0,
        "matches": 0,
        "onlineNow": 0,
        "ownerCount": 3,
        "adminCount": 3,
        "memberCount": 114514
    }
    return "communitySettings: " + json.dumps(settings)

###################### entrance ###########################

QUERY_TYPES = {
    "communities-mainmenupromos": communities_mainmenupromos,
    "communities-getsettings": communities_getsettings
}

def communities_request_dispatch():
    if "qt" not in request.args:
        return bad_request("qt missing in communities.php")

    qt = request.args["qt"]
    if qt in QUERY_TYPES:
        return QUERY_TYPES[qt]()

    return bad_request("unknown qt in communities.php: " + qt)
