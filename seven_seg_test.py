from Adafruit_LED_Backpack.SevenSegment import SevenSegment

display = SevenSegment()
display.begin()

display.clear()
display.print_float(20.00)
display.write_display()
