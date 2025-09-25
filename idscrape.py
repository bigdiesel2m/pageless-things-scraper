import requests

API_URL = "https://oldschool.runescape.wiki/api.php" #we don't need this to change, so might as well set it here
session = requests.Session()
headers = {'User-Agent': 'Automated scraping script to generate list of page IDs on the wiki. See https://github.com/bigdiesel2m/pageless-things-scraper'}

obj_ids = []
offset = 0
while True:
	print(str(offset))
	params = {
		"action": "bucket",
		"format": "json",
		"query": "bucket('object_id').select('id').limit(5000).offset(" + str(offset) + ").run()"
	}
	response_json = session.get(API_URL, params=params, headers=headers).json()
	for result in response_json['bucket']:
		for obj_id in result['id']:
			if obj_id.isnumeric():
				obj_ids.append(str(obj_id))
	if len(response_json['bucket']) == 5000:
		offset = offset + 5000
	else:
		break

with open('obj_ids.txt', "w", encoding="utf-8") as outfile:
	outfile.write('\n'.join(obj_ids))

npc_ids = []
offset = 0
while True:
	print(str(offset))
	params = {
		"action": "bucket",
		"format": "json",
		"query": "bucket('npc_id').select('id').limit(5000).offset(" + str(offset) + ").run()"
	}
	response_json = session.get(API_URL, params=params, headers=headers).json()
	for result in response_json['bucket']:
		for npc_id in result['id']:
			if npc_id.isnumeric():
				npc_ids.append(str(npc_id))
	if len(response_json['bucket']) == 5000:
		offset = offset + 5000
	else:
		break

with open('npc_ids.txt', "w", encoding="utf-8") as outfile:
	outfile.write('\n'.join(npc_ids))