#!python

'''
Interpret .ryf file
'''
import sys
import ryf

try:
	filepath = sys.argv[1]
	if not filepath.endswith('.ryf'):
		ryf.error('Incorrect file extension. must be a .ryf file.')
except IndexError:
	'''Maybe go into interperter??'''
	ryf.error('No file specified.')

def get_cmds(filepath):
	try:
		with open(filepath, 'r') as f:
			contents = f.readlines()
	except:
		ryf.error('That is not a real file!')
	else:
		contents = [c for c in [line.strip() for line in contents] if len(c) > 0]
		'''parse data in file'''
		return ryf.parse(contents)


cmds = get_cmds(filepath)

for cmd in cmds:
	cmd()