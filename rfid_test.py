import spidev
import time
import traceback
from pirc522 import RFID
rf = RFID()
spi = spidev.SpiDev()

spi.open(0, 0)

spi.mode = 0b00
flr = (0x0A << 1)
	# read_mode = [flr|0x80, 0x00]
	# read_mode = [0b10000010, 0x00]
	# write_mode = [0b00000010, 0b00001111]
	# spi.xfer2(write_mode)
	# write_mode = [0x18 <<1&0x7E, 0b00000010]
	# spi.xfer2(write_mode)
	# write_mode = [0x14<<1, 0b0000011]
	# spi.xfer2(write_mode)
	# write_mode = [0x13 <<1&0x7E, 0b10010000]
	# spi.xfer2(write_mode)
	# write_mode = [0x26 << 1,0b01110000]
	# spi.xfer2(write_mode)
	# write_mode = [flr & 0x7E, 0b00000000]
	# spi.xfer2(write_mode)

read_registers = [
	{	
		'name': 'CMD',
		'addr': 0b10000010,
	},
	{	
		'name': 'ERR',
		'addr': (0x06 << 1) | 0x80,
	},
	{	
		'name': 'FIFO Level',
		'addr': flr|0x80,
	},
	{	
		'name': 'Collision',
		'addr': 0x0E << 1 | 0x80,
	},
	{	
		'name': 'Interrupt',
		'addr': 0x04<<1|0x80,
	},
	{	
		'name': 'end',
		'addr': 0x00,
	},
]
def start():
	try:
		write_mode = [0x04<<1& 0x7E, 0b00000000]
		spi.xfer2(write_mode)	
		
		write_mode = [0b00000010, 0b00001000]
		spi.xfer2(write_mode)
		run_command = lambda cmd: rf.dev_write(0x01, cmd)
		poll = 0
		rf.init()
		while True:
			# Transcieve
			# rf.dev_write(0x09, 0x26)
			run_command(0x0C)
			# rf.dev_write(0x0D, 0b10000111)
			# MIFARE Auth
			run_command(0x0E)
			# rf.dev_write(0x0D, 0b10000111)
			vals = spi.xfer2([reg['addr'] for reg in read_registers])
			printRegisters(vals, poll)


			# Wait
			time.sleep(0.8)
			poll += 1
	except:
		print 'Closing...'
		traceback.print_exc()
		spi.close()

def printRegisters(vals, poll):
	print '*********************'
	print '* # {}'.format(poll)
	print '*--------------------'
	for i in xrange(0, len(read_registers) - 1):
		print '* {0}: {1:b}'.format(read_registers[i]['name'], vals[i + 1])
	print '*********************'
start()
