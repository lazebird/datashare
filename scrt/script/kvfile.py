import log
# as dictionary cannot be returned or set arg, this may be changed to use json/dictionary string structure, instead of simple kv structure.
class kvfile:
	def __init__(self, path):
		self.path = path

	def read(self): 
		kvhash = {}
		try :
			f = open(self.path, "r")
			for line in f.readlines():
				line = line.strip()
				args=line.split(' ')
				if len(args) < 2:
					log.err("invalid args: " + line)
					continue
				kvhash[args[0]] = args[1]
			f.close()  
			log.info("reading " + str(kvhash) + " from file " + self.path)
		except:
			log.err("#File "+self.path+" not exists")
		return kvhash

	def write(self, kvhash): # do not support dict as arg?
		log.info("writing " + str(kvhash) + " to file "+ self.path)
		try :
			f = open(self.path, "w") 
			for key in kvhash:
				f.write(key+" "+kvhash[key]+"\n")
			f.close()  
		except:
			log.err("#File "+self.path+" write failed!")
			return 0
		return 1