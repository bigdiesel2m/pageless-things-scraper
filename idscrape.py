import requests

API_URL = "https://oldschool.runescape.wiki/api.php" #we don't need this to change, so might as well set it here
session = requests.Session()
headers = {'User-Agent': 'Automated scraping script to generate list of page IDs on the wiki. See https://github.com/bigdiesel2m/pageless-things-scraper'}

obj_ids = []
for i in range(13): #up to 65000 objects
	offset = 0
	while True:
		print(str(i) + " - " + str(offset))
		bound = i*5000
		params = {
			"action": "ask",
			"format": "json",
			"query": '[[Object ID::>' + str(bound) + ']][[Object ID::<<' + str(bound+5000) + ']]|?Object ID|limit=500|offset=' + str(offset)
		}
		response_json = session.get(API_URL, params=params, headers=headers).json()
		for result in response_json['query']['results']:
			name = result
			for obj_id in response_json['query']['results'][result]['printouts']['Object ID']:
				obj_ids.append(str(obj_id))
		
		if 'query-continue-offset' in response_json:
			offset = response_json['query-continue-offset']
		else:
			break

with open('obj_ids.txt', "w", encoding="utf-8") as outfile:
	outfile.write('\n'.join(obj_ids))

npc_ids = []
for i in range(4): #up to 20000 npcs
	offset = 0
	while True:
		print(str(i) + " - " + str(offset))
		bound = i*5000
		params = {
			"action": "ask",
			"format": "json",
			"query": '[[NPC ID::>' + str(bound) + ']][[NPC ID::<<' + str(bound+5000) + ']]|?NPC ID|limit=500|offset=' + str(offset)
		}
		response_json = session.get(API_URL, params=params, headers=headers).json()
		for result in response_json['query']['results']:
			name = result
			for npc_id in response_json['query']['results'][result]['printouts']['NPC ID']:
				npc_ids.append(str(npc_id))

		if 'query-continue-offset' in response_json:
			offset = response_json['query-continue-offset']
		else:
			break

with open('npc_ids.txt', "w", encoding="utf-8") as outfile:
	outfile.write('\n'.join(npc_ids))