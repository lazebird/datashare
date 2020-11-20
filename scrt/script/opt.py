import log

class opt:
	def __init__(self, obj): # obj: crt.Arguments
		self.obj = obj
		self.opthash = {}
		self.parse_flag = 0

	def parse(self):
		s = ""
		for index in range(self.obj.Count):
			s = s + self.obj[index] + " "
		s = s.replace("#", " ") # support '#' as ' '
		s = s.replace(",", " ") # support ',' as ' '
		s = s.replace("  ", " ") # support '  ' as ' '
		s = s.strip()
		pairs = s.split(" ")
		for tv in pairs:
			args = tv.split("=")
			if len(args) < 2:
				log.err("invalid args: " + tv)
				continue
			self.opthash[args[0]] = args[1]
		self.parse_flag = 1
	
	def tohash(self):
		if not self.parse_flag: 
			self.parse()
		return self.opthash

	def tostr(self):
		if not self.parse_flag: 
			self.parse()
		return str(self.opthash)
