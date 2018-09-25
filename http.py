import requests
import json

from log import log

headers = { 'content-type': 'application/json' }

def postRepetition(weight):
	r = requests.post(
		'http://192.168.1.130:8080/exercises/rep',
		headers=headers,
		data=json.dumps({
			'weight': weight
		})
	)
	log(r.json())
