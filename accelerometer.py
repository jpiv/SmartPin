from pylis.LIS3DH import LIS3DH

from log import log

class Accelerometer(object):
	_sensor = None
	def __init__(self):
		self._sensor = LIS3DH()
		self._sensor.setRange(LIS3DH.RANGE_2G)

	def isGoingUp(self):
		z = self._sensor.getZ()
		return z > 1
