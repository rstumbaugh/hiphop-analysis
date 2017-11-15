import pandas as pd
import numpy as np

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


df_90s = pd.read_csv('90s-charts.csv')
df_10s = pd.read_csv('10s-charts.csv')

for entry in get_top(df_10s, limit=50):
 	print('{} - {} ({} weeks)'.format(entry['artist'], entry['song'], entry['weeks']))