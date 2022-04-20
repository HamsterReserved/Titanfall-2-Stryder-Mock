from wtforms import Form
import config
from . import common_fields

# Common token fields.
# Remember to call super init in your __init__.
class TokenForm(Form):
    env = common_fields.buildEnvField()
    threepToken = common_fields.build3pTokenField()
    NucleusToken = common_fields.buildNucleusTokenField()
    securityToken = common_fields.buildSecurityTokenField()
    allow_empty = False

    def __init__(self, formdata, allow_empty):
        super().__init__(formdata)
        self.allow_empty = allow_empty

    # Note that during nucleus-oauth securityToken is null but NucleusTokenis not.
    # mp.php should do this test itself.
    def tokenValid(self):
        if self["NucleusToken"].data != config.MOCK_NUCLEUS_TOKEN:
            return False
        if self["securityToken"].data != config.MOCK_STRYDER_SECURITY:
            return False
        if self["threepToken"].data != "PC_PLACEHOLDER_3P_TOKEN":
            return False
        return True
