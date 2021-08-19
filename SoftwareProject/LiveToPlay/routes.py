from flask import render_template, session, request, flash, redirect, url_for 
from LiveToPlay.forms import LookUpForm     # for search forms 
from LiveToPlay.models import Tracklist, Track, SpotifyLink
from LiveToPlay import app, db
from TracklistScraper.tracklist import *
import spotipy     # for spotify 
from spotipy.oauth2 import SpotifyOAuth
from SpotifyWebAPI.spotifyAPI import *
import sqlite3   # for database 
from werkzeug.exceptions import abort   # for 404 error
import time


#
# Dummy data 
#
posts = [
	{
		'author' : 'Jane Doe',
		'title' : 'Post Title 1',
		'content' : 'Jane Doe Post 1',
		'date_posted' : '00/00/00'
	},
	{
		'author' : 'John Smith',
		'title' : 'Post Title 2',
		'content' : 'John Smith Post 2',
		'date_posted' : '11/11/11'
	}

]

TOKEN_INFO = "token_info"
clientID = '85492417c1244f0283cc2198c85efa5c'
clientSecret = '94185058d5df4575b529425f8a6945f7'
clientScope = "user-library-read,user-read-currently-playing,playlist-modify-public"

# index/root/homepage
@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts) # pass in posts variable

# about page
@app.route("/about")   
def about():
	sp_oauth = create_spotify_oauth(clientID, clientSecret, clientScope)
	auth_url = sp_oauth.get_authorize_url()
	return redirect(auth_url)     # return the redict URL

# redirect to this page after logging into spotify 
@app.route('/redirect')
def redirectPage():
	sp_oauth = create_spotify_oauth(clientID, clientSecret, clientScope)
	session.clear()
	code = request.args.get('code')
	token_info = sp_oauth.get_access_token(code)
	session[TOKEN_INFO] = token_info  # refresh & access token, and expires
	return redirect(url_for('getTracks', _external=True))

# hellloooo 
@app.route('/gettracks')
def getTracks():
	try:
		token_info = get_token() 
	except:      # exception raised 
		return redirect(url_for('about', _external=True))   # redirect to log in again
	sp = spotipy.Spotify(auth = token_info['access_token'])
	items = sp.current_user_saved_tracks(limit=5, offset=0)['items']
	searchresult = sp.search('artist:Daft Punk track: Burnin', limit=5, offset=0, type='track', market=None)
	track = str([i['track']['name'] for i in items])
	return searchresult["tracks"]
	# return render_template('index.html')

# search page 
@app.route("/search", methods=['GET', 'POST'])
def search():
	form = LookUpForm()
	if form.validate_on_submit():
		try:
			token_info = get_token()
		except:      # exception raised 
			return redirect(url_for('about', _external=True))   # redirect to log in again

		flash(f'Search performed for: {form.url.data}', 'success')
		tracklist = Tracklists(url=form.url.data)   # using url create tracklist object
		sp = spotipy.Spotify(auth = token_info['access_token'])   # get spotipy object
		searchResults = searchSpot(sp, tracklist.tracks)
		spotplaylist = createPlaylist(sp, searchResults, tracklist)
		return redirect(url_for('home'))
	return render_template('search.html', title="Search", form = form)





# Get session token 
# if none exist, need to raise exception
def get_token():
	token_info = session.get(TOKEN_INFO, None)
	if not token_info:
		raise "exception: "
	now = int(time.time())
	is_expired = token_info['expires_at'] - now < 60
	if (is_expired):
		sp_oauth = create_spotify_oauth()
		token_info = sp_oauth.refresh_access_token[token_info['refresh_token']]
	return token_info


