from Adafruit_LED_Backpack.SevenSegment import SevenSegment

class Display(object):
	_display = None
	def __init__(self):
		self._display = SevenSegment()
		self._display.begin()
		self._display.clear()
		self.show(0)

	def show(self, val):
		self._display.clear()
		if type(val) != str:
			self._display.print_float(val)
		else:
			for i, char in enumerate(val):
				self._display.set_digit(i, char)
		self._display.write_display()
