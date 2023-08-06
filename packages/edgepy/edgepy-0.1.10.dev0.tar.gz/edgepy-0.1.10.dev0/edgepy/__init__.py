def setwkdir(dir=''):
	import os
	if (dir==''):
		dir = input('Enter working directory: ')
	
	if (os.isdir(dir)):
		

