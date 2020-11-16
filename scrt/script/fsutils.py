import log
# as dictionary cannot be returned or set arg, this may be changed to use json/dictionary string structure, instead of simple kv structure.
def  loadkvfile(filename): 
	kvhash = {}
	log.info("Loading file: " + filename)
	try :
		f = open(filename, "r")
		for line in f.readlines():
			line = line.strip()
			args=line.split(' ')
			if len(args) < 2:
				log.err("invalid args: " + line)
				continue
			kvhash[args[0]] = args[1]
		f.close()  
		log.info(str(kvhash))
		return str(kvhash) # do not support return dict?
	except:
		log.err("#File "+filename+" not exists")
		return str(kvhash)

def  writekvfile(filename, kvstr): # do not support dict as arg?
	kvhash = eval(kvstr)
	log.info("writing " + str(kvhash) + " to file "+ filename)
	f = open(filename, "w") 
	for key in kvhash:
		f.write(key+" "+kvhash[key]+"\n")
	f.close()  
