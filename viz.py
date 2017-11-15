import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn
matplotlib.style.use('ggplot')

def num_unique_words(lyrics):
	words = re.split(r'\s+', lyrics)
	return len({ word for word in words })

def add_unique_col(df):
	for i,row in df.iterrows():
		num_unique = num_unique_words(row['lyrics'])
		df.set_value(i, 'unique_words', num_unique)
	return df

lyrics_10s = pd.read_csv('10s-lyrics.csv')
lyrics_90s = pd.read_csv('90s-lyrics.csv')

lyrics_10s = add_unique_col(lyrics_10s).drop('lyrics', axis=1)
lyrics_90s = add_unique_col(lyrics_90s).drop('lyrics', axis=1)

lyrics_10s.sort_values('weeks', inplace=True)
lyrics_90s.sort_values('weeks', inplace=True)

print('1990s average unique words: {}'.format(lyrics_90s['unique_words'].mean()))
print('2010s average unique words: {}'.format(lyrics_10s['unique_words'].mean()))

print('1990s average weeks on billboard: {}'.format(lyrics_90s['weeks'].mean()))
print('2010s average weeks on billboard: {}'.format(lyrics_10s['weeks'].mean()))

ax = lyrics_10s.plot('weeks', 'unique_words', kind='scatter')
lyrics_90s.plot('weeks', 'unique_words', kind='scatter', c='r', ax=ax)

plt.show()