from wtforms import Form
from flask import request
from util import bad_request
from . import common_fields

class SubArgs(Form):
    qt = common_fields.buildQtField()

def sub():
    return '''
openInvite:
{
	change: 4
	room: "p_PC_1_1"
	type: "playlist"
	openInviteRoom: "1"
	endTime: 1639928295
	hardware: "PC"
	uid: 1
	creatorName: "Rick"
	playlist: "fd_easy"
	region: "Europe"
	language: "english"
	numSlots: 4
	slotsUsed: 1
	player0h: "PC"
	player0uid: 1
	player0mu: 12.1
	player0icon: 0
	player0name: "Rick"
}
'''

QUERY_TYPES = {
    "sub": sub
}

def sub_request_dispatch():
    args = SubArgs(request.args)
    if not args.validate():
        return bad_request("invalid messages args")

    # TODO: validate session

    qt = request.args["qt"]
    if qt in QUERY_TYPES:
        return QUERY_TYPES[qt]()

    return bad_request("unknown qt in sub")
