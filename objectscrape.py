import requests

API_URL = "https://oldschool.runescape.wiki/api.php" #we don't need this to change, so might as well set it here
session = requests.Session()
headers = {'User-Agent': 'Automated scraping script to generate list of page object IDs on the wiki. See https://github.com/bigdiesel2m/pageless-things-scraper'}
idlist = []

for i in range(13): #up to 65000 objects
	offset = 0
	while True:
		print(str(i) + " - " + str(offset))
		bound = i*5000
		params = {
			"action": "ask",
			"format": "json",
			"query": '[[Object ID::>' + str(bound) +']][[Object ID::<<' + str(bound+5000) +']]'+ '|?Object ID' + '|limit=500' + '|offset=' + str(offset)
		}
		response = session.get(API_URL, params=params, headers=headers)
		responsejson = response.json()
		for result in responsejson['query']['results']:
			name = result
			for id in responsejson['query']['results'][result]['printouts']['Object ID']:
				idlist.append(str(id))
		
		if 'query-continue-offset' in responsejson:
			offset = responsejson['query-continue-offset']
		else:
			break

with open('objidlist.txt', "w", encoding="utf-8") as outfile:
	outfile.write('\n'.join(idlist))