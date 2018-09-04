import time
from pirc522 import RFID

from tags import WeightTag
from log import log

rf = RFID()

def handle_tag(tag):
	# tag.weight = 20
	log('Weight of tag is', tag.weight)
	time.sleep(1.5)

def get_tag():
	rf.request()
	err, uid = rf.anticoll()
	if not err:
		log('Tag read, UID:', uid)
		tag = WeightTag(rf, uid)
		handle_tag(tag)

def detect_tags():
	log('Waiting for tags...')
	while True:
		rf.wait_for_tag()
		get_tag()

def start_loop():
	try:
		detect_tags()
	except:
		log('Stopping...')
		rf.cleanup()
		raise

start_loop()
