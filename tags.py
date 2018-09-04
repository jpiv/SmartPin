from log import log

class Tag(object):
	_key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
	_blocks = 15
	rf = None
	rfutil = None

	def __init__(self, rf, uid, *args, **kwargs):
		self.rf = rf
		self.rfutil = self.rf.util()
		err = self.rfutil.set_tag(uid)
		self.rfutil.auth(self.rf.auth_a, self._key)
		if err:
			log('Error selecting tag')
			return

	def set(self, index, val):
		if index > self._blocks or index < 1:
			raise Exception('`index` param must be between 1-15')
		data = []
		if type(val) == str or type(val) == unicode:
			strVals = [ord(char) for char in val]
			data = strVals
		else:
			data.append(val)

		if len(data) > 16:
			log('Value too long')

		block = []
		for i in xrange(0, 16):
			if i < len(data):
				block.append(data[i])
			else:
				block.append(0)

		err = self.rfutil.do_auth(index)
		err and log('Auth error for write')
		err = self.rf.write(index, block)
		if err:
			log('Error writing to tag')

	def read(self, index):
		err = self.rfutil.do_auth(index)
		if err:
			log('Card auth failed for read')
		else:
			err, data = self.rf.read(index)
			if err:
				log('Error reading card')
			else:
				return data
		return []

	@staticmethod
	def to_string(data):
		return ''.join([
			unichr(byte)
			for byte in data
			if byte != 0
		])

	@staticmethod
	def to_int(data):
		return sum(data)


class WeightTag(Tag, object):
	_block = 1
	_weight = None

	def __init__(self, *args, **kwargs):
		super(WeightTag, self).__init__(*args, **kwargs)

	@property
	def weight(self):
		return Tag.to_int(self.read(self._block))
	
	@weight.setter
	def weight(self, weight):
		self.set(self._block, weight)





