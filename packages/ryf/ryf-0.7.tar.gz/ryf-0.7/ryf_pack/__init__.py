'''
module for util functions
'''
import sys, re
from termcolor import colored

def error(msg, e=None):
	if msg:
		if e:
			print('{}\n{}'.format(colored(e, 'red'), msg))
		else:
			print(msg)
	sys.exit(1)

class Log:
	vars = []


class Command(Log):
	cmds = {
		'show': lambda s: print(s)
	}

	def __init__(self, cmd, arg):
		self.cmd = cmd
		self.arg = arg

	def __call__(self):
		return Command.cmds[self.cmd](self.arg)

	def __repr__(self):
		return '${} : {}'.format(self.cmd, self.arg)


class Variable(Log):
	def __init__(self, name, value):
		self.name = name
		self.value = value
		Log.vars.append(self)

	def is_defined(self):
		return self.name in [v.name for v in Log.vars]

	def __call__(self):
		Log.vars.append(self)

	def __repr__(self):
		return '{} = {}'.format(self.name, self.value)

def get_var(name):
	names = [v.name for v in Log.vars]
	if name in names and len(Log.vars) > 0:
		i = names.index(name)
		return Log.vars[i]
	else:
		return None

def in_string(s):
	return s.startswith('\'') and s.endswith('\'')

def trim(s):
	if in_string(s):
		return s[1:-1]
	else:
		return s

def interpol(line):
	'''string interpolation'''
	data = ' '.join(line.split()[1:])
	pol_regex = r':(\w+):'
	s = re.search(pol_regex, data)
	if s:
		var_name = s.group(1)
		var = get_var(var_name)
		# print(colored(var, 'yellow'))
		if var:
			s = data[:s.start()] + str(var.value) + data[s.end():]
			return trim(s)
		else:
			error('Undefined variable: {}'.format(data), e=line)

def eval(line):
	eval_regex = r'eval ([\w\d]+)\s*([-+/*%])\s*([\w\d]+)'
	s = re.search(eval_regex, line)
	if s:
		ops = {
			'+': lambda l, r: l+r,
			'-': lambda l, r: l-r,
			'*': lambda l, r: l*r,
			'/': lambda l, r: l//r
		}
		l, op, r = s.group(1), s.group(2), s.group(3)

		a = [l, r]
		for i, n in enumerate(a):
			if not n.isdigit():
				# print(colored('{} is not a digit.'.format(n), 'yellow'))
				var = get_var(n)
				if var:
					try:
						a[i] = var.value
					except:
						error('{} is not a number.'.format(var.name), e=line)
				else:
					error('Variable {} has not been declared.', e=line)
		l, r = a
		try:
			return ops[op](int(l), int(r))
		except:
			error('That is not a valid operation.', e=line)
	else:
		return None


def parse(contents):
	stuff = []
	for line in contents:
		# print(line)
		for c in Command.cmds:
			# comments
			if line.startswith('~'):
				continue

			# command (ie. show)
			if line.startswith(c):
				data = ' '.join(line.split()[1:])

				if not in_string(data):
					'''check if the variable has been defined'''
					if data.startswith(':') and data.endswith(':'):
						data = data[1:-1]
					'''check for evaluation'''
					res = eval(data)
					if res != None:
						stuff.append(Command(c, res))
						continue
					try:
						val = get_var(data).value
					except:
						error('Undefined variable: {}'.format(data), e=line)
					else:
						stuff.append(Command(c, val))
						continue

				s = interpol(line)
				if s:
					stuff.append(Command(c, s))
					continue

				msg_regex = r'\'?([-\w\d ,!.;?]*)\'?'
				string = re.search(msg_regex, data).group(1)
				stuff.append(Command(c, string))

			# variable assignment
			elif line.split()[1] == 'is:':
				data = line.split()
				data.pop(1)
				val = ' '.join(data[1:])
				# if not in_string(val) and len(data) > 2:
				# 	error('Too many values in assignment.', e=line)
				name, value = data[0], trim(val)
				
				'''evaluate expression if any'''				
				res = eval(line)
				if res != None:
					stuff.append(Variable(name, res))
				else:
					for v in Log.vars:
						if name == v.name:
							# overwrite the old variable with the new value
							v.value = value
							break
					else:
						stuff.append(Variable(name, value))

			else:
				error('Not a real command.', e=line)
	return stuff
