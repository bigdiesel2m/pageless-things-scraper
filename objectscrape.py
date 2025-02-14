import json
import requests

API_URL = "https://oldschool.runescape.wiki/api.php" #we don't need this to change, so might as well set it here
session = requests.Session()

idlist = []
outlist = []
for i in range(12): #up to 
	offset = 0
	while True:
		print(str(i) + " - " + str(offset))
		bound = i*5000
		params = {
			"action": "ask",
			"format": "json",
			"query": '[[Object ID::>' + str(bound) +']][[Object ID::<<' + str(bound+5000) +']]'+ '|?Object ID' + '|limit=500' + '|offset=' + str(offset)
		}
		response = session.get(API_URL, params=params)
		responsejson = response.json()
		for result in responsejson['query']['results']:
			name = result
			id = responsejson['query']['results'][result]['printouts']['Object ID'][0]
			idlist.append(id)
		
		if 'query-continue-offset' in responsejson:
			offset = responsejson['query-continue-offset']
		else:
			break

with open('idlist.json', 'w') as outfile:
	json.dump(idlist, outfile)
