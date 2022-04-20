# Saves some commonly used fields among different APIs.
# API-specific fields should go to their own form definition.

from wtforms import validators, IntegerField, StringField

def buildQtField():
    return StringField("qt", [validators.Length(1, 100)])

def buildHardwareField():
    return StringField("hardware", [validators.Length(1, 15)]) # PC, PlayStation etc

def buildUidField():
    return IntegerField("uid", [validators.InputRequired()])

def buildLanguageField():
    return StringField("language", [validators.Length(1, 15)])

def buildVerField():
    return IntegerField("ver", [validators.InputRequired()])

def buildTimezoneOffsetField():
    return IntegerField("timezoneOffset", [validators.InputRequired()])

def buildIsTrialField():
    return IntegerField("isTrial", [validators.InputRequired()])

def buildEnvField():
    return StringField("env", [validators.AnyOf(["production"])])

def buildDCField():
    return StringField("dc", [validators.Length(1, 15)])

def buildEAAccessField():
    return IntegerField("EAAccess", [validators.InputRequired(), validators.NumberRange(0, 1)])

class NullableStringField(StringField):
    def pre_validate(self, form):
        if hasattr(form, "allow_empty") and form.allow_empty:
            raise validators.StopValidation

def build3pTokenField():
    return NullableStringField("3pToken", [validators.AnyOf(["PC_PLACEHOLDER_3P_TOKEN"])], name="3pToken")

def buildNucleusTokenField():
    return NullableStringField("NucleusToken", [validators.Length(600, 1024)])

def buildSecurityTokenField():
    return NullableStringField("securityToken", [validators.Length(120, 150)])
