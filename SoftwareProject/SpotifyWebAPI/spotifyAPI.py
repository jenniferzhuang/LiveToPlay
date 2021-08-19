from flask import redirect, url_for, session 
import spotipy     # for spotify 
from spotipy.oauth2 import SpotifyOAuth
from difflib import SequenceMatcher    # string similarity calculator

# returns similarity ratio
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# returns a spotify oauth object
def create_spotify_oauth(clientID, clientSecret, clientScope):
	return spotipy.SpotifyOAuth(
		client_id=clientID,
		client_secret=clientSecret,
		redirect_uri=url_for('redirectPage', _external=True),
		scope=clientScope)

# given a list of spotify items and a track object 
# return spotify item that best matches the track object
def bestFit(queryResult, track):
	tempBest = ""
	tempRatio = -1
	for result in queryResult:
		trackTitle = result["name"]
		ratio = similar(trackTitle, track.title)
		if ratio > tempRatio:
			tempRatio = ratio
			tempBest = result["id"]
	return tempBest

# given a tracklist, perform a search 
# return best fitting search result
def searchSpot(spot_obj, tracks):
	# create empty list of Spotify Track IDs 
	resultTracks = []
	# create list of queries for spotify
	queryList = [t.search_track_query() for t in tracks] 

	# submit search queries
	for query, track in zip(queryList, tracks):
		if (query != ''):      # empty query means it is an ID
			queryResponse = spot_obj.search(query, limit=5, offset=0, type='track', market=None)
			if ("error" not in queryResponse):
				queryResult = queryResponse['tracks']["items"]
			if(len(queryResult) > 0):
				bestfit = bestFit(queryResult, track)
				resultTracks.append(bestfit)
	return resultTracks

def createPlaylist(spot_obj, trackIDList, tracklist):
	user = spot_obj.me()['id']
	print (user + tracklist.title)
	spot_obj.user_playlist_create(user, tracklist.title, public=True, collaborative=False, description='')
	playlist_id = spot_obj.user_playlists(user)["items"][0]['id']
	spot_obj.user_playlist_add_tracks(user, playlist_id, trackIDList)
	return True


