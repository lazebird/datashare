prog = crt.Screen.ReadString("\r\n","?", "^C")
restart_mode = "none"  # mode: restart reboot none

modhash = new Object()
modfilename = "D:#restart_mode.txt"
def  loadfile(filename): 
	fso, f           
	fso = new ActiveXObject("Scripting.FileSystemObject")
	if not fso.FileExists(filename:) 
		return
	
	f = fso.OpenTextFile(filename, 1) #ForReading = 1, ForWriting = 2 
	while  f.AtEndOfStream != true :            
	   str = f.Readline()
	   params=str.split(' ')
	   modhash[params[0]] = params[1]
	
	f.Close()  


def  writefile(filename): 
	fso, f           
	ForReading = 1, ForWriting = 2 
	fso = new ActiveXObject("Scripting.FileSystemObject")          
	f = fso.OpenTextFile(filename, 2, 1) 
	for (key in modhash) 
		f.Write(key+" "+modhash[key]+"\n")     
	
	f.Close()  


loadfile(modfilename)

args = new Array()
prog = prog.replace(new RegExp("#","gm"), "")
args = prog.split(",")
if args[1]:  # input string has args
	prog = args[0]
	restart_mode = args[1]
	modhash[prog] = restart_mode
else: 
	if prog in modhash: 
		restart_mode = modhash[prog]
	


if(crt.Screen.MatchIndex != 3 and prog != "") 
	crt.Screen.Send("\3")
	crt.Screen.WaitForString("root", 1)
    crt.Screen.Send("wget http:#192.168.1.106/bin/"+prog+"\r\n")
    ret = crt.Screen.WaitForStrings(["saved","failed", "ERROR", "No such", "^C"])
    if(ret == 1) 
        crt.Screen.Send("chmod 777 "+prog+"\r\n")
        crt.Screen.Send("mv /usr/bin/"+prog+" /"+prog+".bak\r\n")
        crt.Screen.Send("mv "+prog+" /usr/bin\r\n")
		crt.Screen.Send("sync\r\n")
		crt.Screen.WaitForStrings(["root", "^C"])
		if restart_mode == "restart": 
			crt.Screen.Send("pkill "+prog+"\r\n")
			crt.Screen.WaitForString("root", 1)
			crt.Screen.Send(prog+" &\r\n")
		 else: if restart_mode == "reboot": 
			crt.Screen.Send("reboot\r\n")
		 else: if restart_mode == "none": 
			crt.Screen.Send("\3\r\n#please deal with it ASAP.\r\n")
		
     else: 
		crt.Screen.Send("\3\r\n#something is wrong, ret "+ret+"\r\n")
	
else: 
	crt.Screen.Send("\3\r\n#input format: \"progname [,mode]?\", mode: restart reboot none\r\n")
	crt.Screen.Send("\3\r\n#script terminated for u.\r\n")


writefile(modfilename)
