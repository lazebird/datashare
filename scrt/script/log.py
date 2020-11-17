workdir="D:/"
info_path=workdir+"/info.log"
err_path=workdir+"/error.log"

def init(s):
	global workdir
	global info_path
	global err_path
	workdir=s
	info_path=workdir+"/info.log"
	err_path=workdir+"/error.log"

def info(s): 
	try:
		f = open(info_path, "a") 
		f.write("[Info] " + s + "\n")
		f.close()  
	except:
		print s

def err(s): 
	try:
		f = open(err_path, "a") 
		f.write("[Error] " + s + "\n")
		f.close()  
	except:
		print s
