info_path="D:/info.log"
err_path="D:/error.log"
def  info(s): 
	f = open(info_path, "a") 
	f.write("[Info] " + s + "\n")
	f.close()  

def  err(s): 
	f = open(err_path, "a") 
	f.write("[Error] " + s + "\n")
	f.close()  
