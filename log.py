import sys, os

def log(*args):
	sys.stdout = sys.__stdout__
	print ' '.join([str(arg) for arg in args])
	sys.stdout = open(os.devnull, 'w')
