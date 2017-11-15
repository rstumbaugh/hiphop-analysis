import json

def get_creds(path):
	with open(path, 'r') as f:
		text = ' '.join(f.readlines()).replace('\n', '').replace('\t', '')
		credentials = json.loads(text)
		return credentials

genius_credentials = get_creds('priv/genius-creds.json')