from pylis.LIS3DH import LIS3DH

from log import log

class Accelerometer(object):
	_sensor = None
	def __init__(self):
		self._sensor = LIS3DH()
		self._sensor.setRange(LIS3DH.RANGE_2G)
		self._zeros = self.getForces()
		self.orientation = 1
		self.up = 0
		self.down = 0
		self.peak = 0
		self.finish = 0

	def getForces(self):
		return [
			self._sensor.getX(),
			self._sensor.getY(),
			self._sensor.getZ(),
		]

	def setZeros(self):
		self._zeros = self.getForces()

	def isRepComplete(self):
		mag = self.getMagnitude()
		ori = mag and mag / abs(mag)
		upCount = 7
		peakCount = 5
		downCount = 5
		finishCount = 3
		threshUp = 1
		threshDown = 2.2
		threshPeak = 0.5
		threshBottom = 0.5
		log(self.up, self.peak, self.down, self.finish, mag, ori, self.orientation)
		if (self.up <= upCount and abs(mag) > threshUp):
			self.up += 1
		elif (self.up > upCount and self.peak <= peakCount and abs(mag) < threshPeak):
			self.peak += 1
			self.orientation = ori
		elif (self.peak > peakCount and self.down <= downCount and abs(mag) > threshDown):
			self.down += 1
			self.orientation = ori
		elif (self.finish <= finishCount and self.up > upCount and self.down > downCount and self.peak > peakCount and abs(mag) < threshBottom):
			self.finish += 1
		elif (self.finish > finishCount and self.up > upCount and self.down > downCount and self.peak > peakCount and abs(mag) < threshBottom):
			self.setZeros()
			self.up = 0
			self.peak = 0
			self.down = 0
			self.finish = 0
			return True


	def getMagnitude(self):
		forces = self.getForces()
		# meters / second
		acceleration = [
            round(abs(forces[0] - self._zeros[0]) * 9.8, 2),
            round(abs(forces[1] - self._zeros[1]) * 9.8, 2),
            round(abs(forces[2] - self._zeros[2]) * 9.8, 2),
 		]
 		return max(acceleration)
