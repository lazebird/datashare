srvip = "192.168.100.106"#"10.1.1.2"
if crt.Arguments.Count > 0:
    srvip = crt.Arguments[0]

prog = crt.Dialog.Prompt("Please enter binary name; format: name [,mode]; mode: restart reboot none") # prog = crt.Screen.ReadString({"\r\n","?", "^C"})
restart_mode = "none"  # mode: restart reboot none
modhash = {}
modfilename = "D:/restart_mode.txt"

def optparse(s):
	global prog
	global restart_mode
	global modhash
	s = s.replace("#", ",") # support '#' as ','
	args = s.split(",")
	if len(args) > 1:  # input string has args
		prog = args[0]
		restart_mode = args[1]
		modhash[prog] = restart_mode
	else: 
		if prog in modhash: 
			restart_mode = modhash[prog]

def  loadmodefile(filename): 
	try :
		f = open(filename, "r")
		for line in f.readlines():
			line = line.strip()
			params=line.split(' ')
			modhash[params[0]] = params[1]
		f.close()  
	except:
		crt.Screen.Send("#File "+filename+" not exists")

def  writemodefile(filename): 
	f = open(filename, "w") 
	for key in modhash:
		f.write(key+" "+modhash[key]+"\n")     
	f.close()  

def do_load(prog, restart_mode):
	if prog == "":
		crt.Screen.Send("\3\r\n#invalid input\r\n")
		crt.Screen.Send("\3\r\n#script terminated for u.\r\n")
		return

	crt.Screen.Send("\3")
	crt.Screen.WaitForString("root", 1)
	crt.Screen.Send("wget http://"+srvip+"/bin/"+prog+"\r\n")
	ret = crt.Screen.WaitForStrings(["saved","failed", "ERROR", "No such", "^C"])
	if ret == 1:
		crt.Screen.Send("chmod 777 "+prog+" && mv /usr/bin/"+prog+" /"+prog+".bak && mv "+prog+" /usr/bin && sync\r\n")
		crt.Screen.WaitForStrings(["root", "^C"])
		if restart_mode == "restart": 
			crt.Screen.Send("pkill "+prog+"\r\n")
			crt.Screen.WaitForString("root", 1)
			crt.Screen.Send(prog+" &\r\n")
		elif restart_mode == "reboot": 
			crt.Screen.Send("reboot\r\n")
		elif restart_mode == "none": 
			crt.Screen.Send("\3\r\n#please deal with it ASAP.\r\n")
	else: 
		crt.Screen.Send("\3\r\n#something is wrong, ret "+ret+"\r\n")

loadmodefile(modfilename)
optparse(prog)
writemodefile(modfilename)
do_load(prog, restart_mode)
