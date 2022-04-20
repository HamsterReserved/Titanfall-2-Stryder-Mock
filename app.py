from flask import Flask
from pages import communities, mp, nucleus_oauth, emptyservers, me, messages, sub
import util

app = Flask(__name__)

@app.route("/communities.php", methods=["POST"])
def communities_page():
    return communities.communities_request_dispatch()

@app.route("/mp.php", methods=["POST"])
def mp_page():
    return mp.mp_request_dispatch()

@app.route("/nucleus-oauth.php", methods=["POST"])
def nucleus_oauth_page():
    util.multipart_fixup() # Only this request is troublesome
    return nucleus_oauth.nucleusOAuth_request_dispatch()

@app.route("/emptyservers/", methods=["POST"])
def emptyservers_page():
    return emptyservers.emptyservers_request_dispatch()

@app.route("/me.php", methods=["POST"])
def me_page():
    return me.me_request_dispatch()

@app.route("/messages.php", methods=["POST"])
def messages_page():
    return messages.messages_request_dispatch()

@app.route("/sub/<subid>", methods=["GET"])
def sub_page():
    return sub.sub_request_dispatch()
