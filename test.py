from pirc522 import RFID
import traceback

rf = RFID()
util = rf.util()
rf.init()
util.debug = True
while True:
    print 'waiting for tag...32'

    rf.wait_for_tag()
    
    err, data = rf.request()
    if not err:
        print 'Tag read'
    else:
    	traceback.print_exc()
        print 'error'


