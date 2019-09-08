import sys
from spotipy import *

def query(spotify, artist):
    return spotify.search(artist, type="artist")

if __name__ == "__main__":
    print(query(sys.argv[1]))
