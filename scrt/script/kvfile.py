import log
# as dictionary cannot be returned or set arg, this may be changed to use json/dictionary string structure, instead of simple kv structure.
class kvfile:
	def __init__(self, path):
		self.path = path

	class kvitem:
		def __init__(self, k, v):
			self.key = k
			self.val = v

	def read(self): 
		kvlist = []
		try :
			f = open(self.path, "r")
			for line in f.readlines():
				line = line.strip()
				args=line.split(' ')
				if len(args) < 2:
					log.err("invalid args: " + line)
					continue
				kvlist.append(self.kvitem(args[0], args[1]))
			f.close()  
			log.info("reading " + str(kvlist) + " from file " + self.path)
		except:
			log.err("#File "+self.path+" not exists")
		return kvlist

	def findval(self, kvlist, k):
		for item in kvlist:
			if item.key == k:
				return item.val
		return None

	def getlastkey(self, kvlist):
		if len(kvlist) <= 0:
			return None
		return kvlist[-1].key
	
	def setitem(self, kvlist, k, v):
		for item in kvlist:
			if item.key == k:
				kvlist.remove(item)
		item = self.kvitem(k, v)
		kvlist.append(item)

	def write(self, kvlist): # do not support dict as arg?
		log.info("writing " + str(kvlist) + " to file "+ self.path)
		try :
			f = open(self.path, "w") 
			for item in kvlist:
				f.write(item.key+" "+item.val+"\n")
			f.close()  
		except:
			log.err("#File "+self.path+" write failed!")
			return 0
		return 1