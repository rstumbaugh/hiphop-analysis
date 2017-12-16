import json

def get_creds(path):
	with open(path, 'r') as f:
		text = ' '.join(f.readlines()).replace('\n', '').replace('\t', '')
		credentials = json.loads(text)
		return credentials

genius_credentials = get_creds('priv/genius-creds.json')

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
    'Dis `N\' Dat Feat. 95 South,69 Boyz & K-Nock - Freak Me Baby': '/Dis-n-dat-party-lyrics',
    'Kanye West, Big Sean, Pusha T, 2 Chainz - Mercy': '/Kanye-west-mercy-lyrics'
}

