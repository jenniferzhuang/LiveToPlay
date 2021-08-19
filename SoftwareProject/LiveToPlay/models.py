#
# this file creates the tables and relationships for the app
#

#
# uses sql alchemy (in the app, an ORM object relational mapper, using object oriented way)
# uses SQL LITE 
#


#
# create database
# python3
# from LiveToPlay import db
# db.create_all()
# from LiveToPlay.models import tracklist, track, spotifylink
# creates a database called site.db in the project directory (this is SQL lite )
#

from datetime import datetime
from LiveToPlay import db

# tracklist table
class Tracklist(db.Model):
	__tablename__ = 'tracklist'
	tracklist_id = db.Column(db.Integer, primary_key=True)
	tracklist_url = db.Column(db.String(500), nullable=False, default="URL")
	tracklist_title = db.Column(db.String(200), nullable=False, default="NAME")
	tracklist_artist = db.Column(db.String(100), nullable=False, default="ARTIST")
	tracklist_content = db.Column(db.String(300), nullable=False, default="CONTENT")
	tracklist_performance_type = db.Column(db.String(100), nullable=False, default="PER_TYPE")
	tracklist_numtracks = db.Column(db.Integer, nullable=False, default=0)
	# relationship
	tracklist_tracks = db.relationship('Track', backref='tracklist_track', lazy=True)
	tracklist_spotLink = db.relationship('SpotifyLink', backref='tracklist_spotify', lazy=True)

	def __repr__(self):
		return f"Set('{self.tracklist_content}')"

# song table
class Track(db.Model):
	__tablename__ = 'track'
	track_id = db.Column(db.Integer, primary_key=True)
	track_full_title = db.Column(db.String(200), nullable=False, default="FULL_TITLE")
	track_title = db.Column(db.String(100), nullable=False, default="TITLE")
	track_musicLabel = db.Column(db.String(100), nullable=False, default="LABEL")
	tracklist_artist = db.Column(db.String(100), nullable=False, default="LABEL")
	# foreign key, many to one relationship 
	track_tracklist_id = db.Column(db.Integer, db.ForeignKey('tracklist.tracklist_id'), nullable=False)
	
	def __repr__(self):
		return f"Song('{self.track_full_title}')"

# Spotify link song table
class SpotifyLink(db.Model):
	__tablename__ = 'spotify_link'
	link_id = db.Column(db.Integer, primary_key=True)
	link_url = db.Column(db.String(500), nullable=False, default="URL")
	link_numtracks = db.Column(db.Integer, nullable=False, default=0)
	# foreign key
	link_tracklist_id = db.Column(db.Integer, db.ForeignKey('tracklist.tracklist_id'), nullable=False)

	def __repr__(self):
		return f"SpotifyLink('{self.link_url}')"