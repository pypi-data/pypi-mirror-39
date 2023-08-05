
def clear(dir):
	import os, glob
	files = glob.glob(dir+'/*')
	for f in files:
		os.remove(f)


def cleanws():
	import os
	ogdir = os.getcwd()
	os.chdir('../docs/workspace')
	clear(os.getcwd())


def test():
	import os
	print(os.getcwd())


