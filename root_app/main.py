import sys
from flask import Flask, request, redirect, render_template, url_for, flash, make_response
import requests
import json
import datetime
from urllib.parse import quote

if len(sys.argv) >= 2 and sys.argv[1] == "local":
    from config import *
    from forms import *
    from engine import *
else:
    from .config import *
    from .forms import *
    from .engine import *
# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.

app = Flask(__name__, static_url_path = '/static')
app.config['SECRET_KEY'] = SECRET_KEY
app.config.broker_url = 'redis://localhost:6379/0'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if len(sys.argv) >= 2 and sys.argv[1] == "local":
    CLIENT_SIDE_URL = "http://0.0.0.0:" + str(PORT)
else:
    CLIENT_SIDE_URL = "http://spotify-sharp.herokuapp.com"

REDIRECT_URI = "{}/callback/q".format(CLIENT_SIDE_URL)
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

@app.route("/", methods = ['GET', 'POST'])
def index():

    global EXPIRE
    if "token" not in request.cookies:
        #TODO: fix the pesky timezone issue
        expire = datetime.datetime.now() + datetime.timedelta(hours=4, seconds=EXPIRE)
        resp = make_response(redirect('authorize'))
        # This is to take care of issues from users pressing the back button
        # If somebody has a better solution, by all means lmk :D
        #resp.set_cookie('owner', 'junk', expires = expire)
        return resp

    bpm_form = BPMForm()
    all_tracks_form = AllTracksForm()

    bpm_form.bpm.choices = [(i, (str(i) + " BPM")) for i in range(MINIMUM_TEMPO, MAXIMUM_TEMPO, STEP_TEMPO)]


    if all_tracks_form.validate_on_submit():
        add_all(all_tracks_form.artist.data, request.cookies["token"])
        flash("Successfully added all tracks by {}".format(all_tracks_form.artist.data))
        resp = make_response(redirect(url_for('index')))
        #expire = datetime.datetime.now() + datetime.timedelta(hours=4, seconds=EXPIRE)
        #resp.set_cookie('token', request.cookies["token"], expires=expire)
        return resp

    if bpm_form.validate_on_submit():
        success, num_tracks = add_bpm(bpm_form.bpm.data, request.cookies["token"])
        if success and num_tracks > 0:
            flash("Successfully added {} track{}".format(num_tracks, 's' if num_tracks > 1 else ''))
            flash("Check your playlists on Spotify :)")
        elif not success:
            flash("An unexpected error occurred", 'error')
            flash("Please contact the developer at sanchitb@buffalo.edu", 'error')
        else:
            flash("Did not find any matching tracks, please try saving more tracks or choosing a different BPM")

        resp = make_response(redirect(url_for('index')))
        #expire = datetime.datetime.now() + datetime.timedelta(hours=4, seconds=EXPIRE)
        #resp.set_cookie('token', request.cookies["token"], expires=expire)
        return resp

    print(bpm_form.errors, flush=True)
    return render_template('index.html', bpm_form = bpm_form, all_tracks_form = all_tracks_form)

@app.route("/cron/")
def cron():
    '''
    Since the index page redirects the user directly to the authorize link,
    figured I'd use a separate URL to keep the Heroku dyno alive
    '''
    return "<h1></h1>"

@app.route("/authorize")
def authorize():
    '''
    if "owner" not in request.cookies:
        return redirect(url_for('index'))
    '''
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():

    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    resp = make_response(redirect(url_for('index')))

    global EXPIRE
    EXPIRE = expires_in

    expire = datetime.datetime.now() + datetime.timedelta(hours=4, seconds=expires_in)
    resp.set_cookie('token', access_token, expires=expire)

    return resp

if __name__ == "__main__":
    app.run(debug=True, port=PORT, threaded = True)
