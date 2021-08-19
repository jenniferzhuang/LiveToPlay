from TracklistScraper.scraper import *
import re    # for regular expressions

# full title
# title 
# music label
# artists
class Tracks:
	def __init__(self, track_content):
		# set full content
		self.full_title = track_content
		split = track_content.split(" - ")
		artists = split[0].replace('ft.', '&').replace('vs.', '&').split("&")
		# set title of song
		self.title = split[1].split("  ")[0]
		# set label of song
		if(len(split[1].split("  ")) > 1):
			if(split[1].split("  ")[1].strip() != ""):
				self.label = split[1].split("  ")[1].title()
			else:
				self.label = "NONE"
		else:
			self.label = "NONE"
		# set artists
		self.artists = [a.strip() for a in artists]

	def search_track_query(self):
		if(self.title.strip() == 'ID'):
			return ''
		# add artist query
		query = 'artist:' + ' AND '.join(self.artists)
		# add track name
		query = query + ' track:' + self.title.replace('\xa0', ' ')
		return query

	def __repr__(self):
		return self.full_title.strip()

# url 
# title 
# artists 
# content
# performance_type
# performance_length
# tracks (list)
# num tracks   -- includes IDs (but ids are not in the tracks)
# date
# genres
class Tracklists:
	def __init__(self, url):
		# use scraper and get html content from url
		soup = get_soup(url);
		# set attributes
		self.url = url
		
		self.title = soup.find("title").get_text()
		
		authors = soup.find_all("meta", {"itemprop": "author"})
		authors = authors[1:]
		self.artists = [a['content'] for a in authors]
		
		self.content = soup.find("meta", {"property": "og:description"})
		content_split = self.content['content'].split(',')
		self.performance_type = content_split[0]
		self.performance_length = content_split[2]
		self.genres = content_split[3:]

		self.num_tracks = soup.find("meta", {"itemprop": "numTracks"})['content'];
		
		tracks = soup.find_all("div", attrs={"class": "fontL", "itemprop": "tracks"})
		self.tracks = [Tracks(t.get_text()) for t in tracks]

	def __repr__(self):
		return self.content

