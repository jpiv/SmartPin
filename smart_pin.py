import time
from pirc522 import RFID

from tags import WeightTag
from display import Display
from accelerometer import Accelerometer
from log import log
import http

rf = RFID()
display = Display()
accel = Accelerometer()
tagWeight = 0

def handle_tag(tag):
	# tag.weight = 20
	global tagWeight
	weightRead = tag.weight
	if weightRead and weightRead != tagWeight:
		display.show(weightRead)
	if weightRead:
		tagWeight = tag.weight


def get_tag():
	rf.request()
	err, uid = rf.anticoll()
	if not err:
		# log('Tag read, UID:', uid)
		tag = WeightTag(rf, uid)
		handle_tag(tag)


def detect_tags():
	log('Waiting for tags...')
	while True:
		# rf.wait_for_tag()
		if accel.isRepComplete():
			display.show('FFFF')
			http.postRepetition(tagWeight)
			time.sleep(1)
			display.show('0000')

		# new thread here
		# rf.init()
		# get_tag()


def start_loop():
	try:
		detect_tags()
	except:
		log('Stopping...')
		rf.cleanup()
		raise

start_loop()
