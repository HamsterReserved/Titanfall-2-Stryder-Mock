Titanfall 2 Stryder Mock Server
===

Mocks stryder communication for the Titanfall 2 game. HTTPS interception of `*.respawn.com` is required but out of the scope of this repository.

Only the minimum set of requests for loading into MP lobby has been implemented, but with basic integrity check and authentication. Most of the responses are hardcoded at this time.

#### Server deployment

If you just want to be quick:

1. Launch a R2Northstar server with `+map mp_lobby` and no other arguments. Also check ns_startup_args{,_dedi}.txt to be sure.
2. Modify config.py so that it points to your R2Northstar server
3. Execute the following:

```sh
pip3 install -r requirements.txt
flask run
```

Refer to [Flask documentation](https://flask.palletsprojects.com/en/2.1.x/deploying/) for proper deployment (if you must :-) this repo has only been a proof-of-concept so far)

#### Client setup

Detailed guide TBD. Here are some tools you might find useful:

* Clash for Windows (in fake-ip mode, for redirecting game requests to Fiddler, installed along with the game)
* Fiddler Classic (for AutoResponder forwarding requests to Flask, installed on another computer)

Don't even try to install these two on the same computer, unless you have absolutely run out of ideas about how to spend your night.
