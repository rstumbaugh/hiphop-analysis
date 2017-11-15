import re
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import urllib.parse as urllib
from load_credentials import genius_credentials

# irregular cases that had to be manually fetched
fetched_urls = {
	'G-Eazy x Bebe Rexha - Me, Myself & I': '/G-eazy-me-myself-and-i-lyrics',
	'A$AP Rocky Featuring Drake, 2 Chainz & Kendrick Lamar - F**kin Problems': '/A-ap-rocky-fuckin-problems-lyrics',
	'2Pac Featuring K-Ci And JoJo - How Do U Want It/California Love': '/2pac-how-do-u-want-it-lyrics',
	'Coolio Featuring L.V. - Gangsta\'s Paradise (From "Dangerous Minds")': '/Coolio-gangstas-paradise-lyrics',
	'12 Gauge - Dunkie Butt (Please Please Please)': '/12-gauge-dunkie-butt-by-12-gauge-lyrics',
	'The Notorious B.I.G. - Big Poppa/Warning': '/The-notorious-big-big-poppa-lyrics',
	'Jay-Z Featuring Foxxy Brown - Ain\'t No Nigga/Dead Presidents': '/Jay-z-aint-no-nigga-lyrics',
	'MC Lyte Featuring Xscape - Keep On, Keepin\' On (From "Sunset Park")': '/Mc-lyte-keep-on-keepin-on-lyrics',
	'95 South - Rodeo': 'local:lyrics/rodeo.txt',
	'Busta Rhymes - Woo-Hah!! Got You All In Check/Everything Remains Raw': '/Busta-rhymes-woo-hah-got-you-all-in-check-lyrics',
	'Cypress Hill - The Phuncky Feel One/How I Could Just Kill A Man': '/Cypress-hill-the-phuncky-feel-one-lyrics',
	'Dis `N\' Dat Feat. 95 South,69 Boyz & K-Nock - Freak Me Baby': '/Dis-n-dat-party-lyrics'
}

match_threshold = 0.75
search_results_weight = 0.2

# frequently-used regular expressions
multi_space_regex = re.compile('\s+')
punctuation_regex = re.compile('[\'"/:;,&]')
features_regex = re.compile(r'Feat((uring)|(\.)) .+', re.IGNORECASE)
lyrics_info_regex = re.compile(r'\[.+?\/]')
auth_header = { 'Authorization': 'Bearer {}'.format(genius_credentials['access_token']) }

def get_top(df, limit=10):
	weeks = {}
	for (index, row) in df.iterrows():
		artist = row['artist']
		song = row['title']
		if (artist,song) in weeks:
			weeks[(artist,song)] += 1
		else:
			weeks[(artist,song)] = 1
	sorted_keys = sorted(weeks, key=weeks.get, reverse=True)[:limit]
	return [{ 'artist': artist, 'song': song, 'weeks': weeks[artist,song]} for (artist,song) in sorted_keys]

def strip_punctuation(string):
	string = punctuation_regex.sub(' ', string)
	return multi_space_regex.sub(' ', string)

def get_match_pct(full_title, artist, song):
	''' Returns percent match of artist and song in full title '''
	terms = artist.split(' ') + song.split(' ')
	found = 0
	for term in terms:
		if term.lower() in full_title.lower():
			found += 1

	return found / len(terms)

def search_genius_url(artist, song):
	''' Gets best match for artist, song by searching on Genius.com '''
	url = 'https://api.genius.com/search?q={}'
	artist = features_regex.sub('', artist)
	artist = strip_punctuation(artist) 

	query = multi_space_regex.sub(' ', '{} {}'.format(artist, song))
	url = url.format(urllib.quote(query))
	response = requests.get(url, headers=auth_header)
	if response.status_code != 200:
		print('Bad response: {} - {}'.format(artist, song))
		return None
	
	# start looking for best match out of all search results
	best_match = None
	max_match_pct = 0
	hits = response.json()['response']['hits']
	num_hits = len(hits)
	for i in range(num_hits):
		hit = hits[i]
		if hit['type'] != 'song':
			continue
		result = hit['result']
		full_title = result['full_title']

		# match percentage takes into account artist, song, and order in search results 
		match = get_match_pct(full_title, artist, song)
		match *= 1 - search_results_weight
		match += search_results_weight * (num_hits - i) / num_hits

		if match > match_threshold and match > max_match_pct:
			best_match = result
			max_match_pct = match 

	return best_match

def scrape_lyrics(path):
	if path.startswith('local:'):
		path = path[6:]
		with open(path, 'r') as f:
			lyrics = ' '.join(f.readlines()).replace('\n', '').replace('\t', '')
	else:
		url = 'https://genius.com{}'.format(path)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		lyrics = soup.find(class_='lyrics').text
		lyrics = lyrics_info_regex.sub('', lyrics)
	return multi_space_regex.sub(' ', lyrics)

def scrape_all_songs(charts_df):
	lyrics_list = []
	for entry in get_top(charts_df, limit=50):
		artist, song, weeks = entry['artist'], entry['song'], entry['weeks']
		if '{} - {}'.format(artist, song) in fetched_urls:
			match = {'path': fetched_urls['{} - {}'.format(artist, song)]}
		else:
			match = search_genius_url(artist, song)
		if match is None:
			print('No match found: {} - {}'.format(artist, song))
			continue
		lyrics = scrape_lyrics(match['path'])
		lyrics_list.append({
			'artist': artist,
			'song': song,
			'weeks': weeks,
			'lyrics': lyrics
		})
		print('Added {} - {}'.format(artist, song))
	
	return lyrics_list

df_90s = pd.read_csv('90s-charts.csv')
df_10s = pd.read_csv('10s-charts.csv')

lyrics = scrape_all_songs(df_90s)
pd.DataFrame(lyrics).to_csv('90s-lyrics.csv')