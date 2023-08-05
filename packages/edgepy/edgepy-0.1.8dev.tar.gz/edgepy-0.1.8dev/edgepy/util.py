
def clear(dir):
	import os, glob
	files = glob.glob(dir+'/*')
	for f in files:
		os.remove(f)


def cleanws():
	from edgepy import Disp
	import os
	ogdir = os.getcwd()
	mdir = Disp.__file__
	os.chdir(mdir)
	os.chdir('..')
	os.chdir('..')
	os.chdir(os.getcwd() + '/docs/workspace')
	clear(os.getcwd())
	os.chdir(ogdir)


def test():
	from edgepy import Disp
	import os
	mdir = Disp.__file__
	os.chdir(mdir)
        os.chdir('..')
        os.chdir('..')
        os.chdir(os.getcwd() + '/docs/workspace')
	print(os.getcwd())



