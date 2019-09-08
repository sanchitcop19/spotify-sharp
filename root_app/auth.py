from spotipy import util as util
import os
import sys
if len(sys.argv) >= 2 and sys.argv[1] == "local":
    from config import *
else:
    from .config import *


def get_token():
    try:
        token = util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    except (AttributeError):
        print("Error")
        os.remove(f".cache-{username}-{SCOPE}")
        token = util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    if not token:
        print("no token")
        sys.exit()
    return token
