from flask import Flask, request, url_for, session, redirect
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import time
import pandas as pd

app = Flask(__name__)

app.secret_key = 'Slickkiller27'
app.config['SESSION_COOKIE_NAME']= "Adis Cookie"
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    auth = createSpotifyOAuth()
    auth_url = auth.get_authorize_url()
    return redirect(auth_url)

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return('/')

@app.route('/redirect')
def redirectPage():
    auth = createSpotifyOAuth()
    session.clear()
    code = request.args.get('code')
    token_info = auth.get_access_token(code)
    session[TOKEN_INFO] = token_info

    return redirect(url_for("getTracks", external = True))

@app.route('/getTracks')
def getTracks(): 
    try: 
        token_info = get_token()
    except:
        print("user is not logged in")
        return redirect(url_for("login", exeternal = True))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.current_user_saved_tracks()
    loop = 0
    allSongs = []
    while True: 
        songsToBeAdded = sp.current_user_saved_tracks(limit= 50, offset= loop * 50)["items"]
        for idx, song in enumerate(songsToBeAdded):
            track = song['track']
            songName = track['name'] + " - " + track['artists'][0]['name']
            allSongs += [songName]
        if (len(songsToBeAdded) < 50): #means we reached end of playlist
            break
    df = pd.DataFrame(allSongs, columns= ["song title"])
    df.to_csv("songs.csv", index= False)
   
    return "We successfuly downloaded " + str(len(allSongs)) + " songs to csv file"


def get_token(): 
    token_info = session.get(TOKEN_INFO, None) #if value doesn't exist return none
    print(token_info)
    if not token_info:
        raise "exception"
    currentTime = int(time.time())
    isExpired = token_info['expires_at'] - currentTime < 60
    if (isExpired):
        auth = createSpotifyOAuth()
        token_info = auth.refresh_access_token(token_info['refresh_token'])
    return token_info


clientID = "b609faeca69c47ce9351cf1c38e00d31"
clientSecretKey = "18816f033ccf4ec2ad5ba71d032921aa"

def createSpotifyOAuth():
    return SpotifyOAuth(
        client_id="b609faeca69c47ce9351cf1c38e00d31",
        client_secret="18816f033ccf4ec2ad5ba71d032921aa",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read"

    )

