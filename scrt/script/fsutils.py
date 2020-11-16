import log
def  loadkvfile(filename, kvhash): 
	try :
		f = open(filename, "r")
		for line in f.readlines():
			line = line.strip()
			args=line.split(' ')
			if len(args) < 2:
				log_err("invalid args: " + line)
				continue
			kvhash[args[0]] = args[1]
		f.close()  
		return kvhash
	except:
		log_err("#File "+filename+" not exists")
		return kvhash

def  writekvfile(filename, kvhash): 
	f = open(filename, "w") 
	for key in kvhash:
		f.write(key+" "+kvhash[key]+"\n")
	f.close()  
