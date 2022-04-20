import re
from flask import make_response, request
from werkzeug.datastructures import MultiDict
from requests_toolbelt.multipart import decoder
import config

# Form a response with msg as HTTP 400 to user, save (logmsg||msg) in log.
def bad_request(logmsg=None, msg=None):
    if msg is None:
        #msg = "Go away."
        msg = logmsg
    if logmsg is None:
        logmsg = msg

    # TODO: logging
    return make_response(msg, 400)

# Parse request body if it's multipart/form-data. Leave as is otherwise.
# This parser properly supports the game's broken formdata format.
def multipart_fixup():
    parts = None
    content_type = request.headers["content-type"]
    if "multipart/form-data" in content_type:
        req_len = int(request.headers["content-length"])
        if req_len <= config.MAX_MULTIPART_FORMDATA_POST_LENGTH:
            raw_data = request.get_data(
                cache=True, as_text=False, parse_form_data=False)
            decoder_i = decoder.MultipartDecoder(raw_data, content_type)
            for v in decoder_i.parts:
                # Dunno whatsup with these encodings
                name = re.findall(
                    'name="([^"]+)"', v.headers[b"Content-Disposition"].decode("utf-8"))[0]
                if parts is None:
                    parts = {}
                parts[name] = v.text
    if parts is not None:
        request.form = MultiDict(parts)
