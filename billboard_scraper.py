import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

def scrape_billboard(start_url, end_url):
	result = []
	current_url = start_url
	while current_url != end_url:
		print('checking ' + current_url)
		year, month, week = current_url[50:54], current_url[55:57], current_url[58:]
		response = requests.get(current_url)
		soup = BeautifulSoup(response.text, 'html.parser')
		chart_items = soup.find_all('article', class_='chart-row')
		for row in chart_items:
			ranking = row.find('span', class_='chart-row__current-week').text.strip()
			title = row.find('h2', class_='chart-row__song').text.strip()
			artist = row.find(class_='chart-row__artist').text.strip()
			result.append({
				'rank': ranking,
				'title': title,
				'artist': artist,
				'week': '{}-{}-{}'.format(year, month, week)
			})
		
		nav = soup.find('nav', class_='chart-nav')
		if nav is None:
			print('can\'t find nav, trying again...')
			time.sleep(1)
		else:
			next_url = nav.find('a', {'data-tracklabel': 'Week-next'})['href']
			next_url = 'http://www.billboard.com' + next_url
			current_url = next_url
	return pd.DataFrame(result)

# want to scrape 87-97, 2007-2017
start_90s = 'http://www.billboard.com/charts/rap-song/1990-01-06'
end_90s   = 'http://www.billboard.com/charts/rap-song/1998-01-03'

# charts_90s = scrape_billboard(start_90s, end_90s)
# charts_90s.to_csv('90s-charts.csv')

start_10s = 'http://www.billboard.com/charts/rap-song/2010-01-02'
end_10s = 'http://www.billboard.com/charts/rap-song/2017-11-25'

charts_10s = scrape_billboard(start_10s, end_10s)
charts_10s.to_csv('10s-charts.csv')