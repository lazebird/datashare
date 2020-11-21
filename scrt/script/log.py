import os.path

class log(object):
	_instance = None
	logpath = None
	def __new__(cls, *args, **kw): # single instance
		if cls._instance is None:
			cls._instance = object.__new__(cls, *args, **kw)
		return cls._instance

	def __init__(self, logpath=None):
		if not logpath and not self.logpath:
			logpath="D:/pyscript.log" if os.path.isdir("D:/") else "/tmp/pyscript.log"
		if logpath:
			self.logpath = logpath

	def info(self, s): 
		try:
			f = open(self.logpath, "a") 
			f.write("[Info] " + s + "\n")
			f.close()  
		except:
			print s

	def err(self, s): 
		try:
			f = open(self.logpath, "a") 
			f.write("[Error] " + s + "\n")
			f.close()  
		except:
			print s

def info(s):
	log().info(s)

def err(s):
	log().err(s)
