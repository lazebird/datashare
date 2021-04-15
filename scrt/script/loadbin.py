import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import log
import kvfile
import opt

opthash = opt.opt(crt.Arguments).tohash()

srvip = "192.168.100.106"#"10.1.1.2"
if crt.GetActiveTab().Caption.find("serial") >= 0: # local serial port
	srvip = "2.2.2.106" 

workdir="D:/" if os.path.isdir("D:/") else "/var/lib"
if "ip" in opthash:
	srvip = opthash["ip"]
if "workdir" in opthash:
	workdir = opthash["workdir"]

def modeparse(s, modlist):
	global prog
	global restart_mode
	global f
	s = s.replace("#", " ") # support '#' as ' '
	s = s.replace(",", " ") # support ',' as ' '
	s = s.replace("  ", " ") # remove extra separator
	args = s.split(" ")
	if len(args) > 1:  # input string has args
		prog = args[0]
		restart_mode = args[1]
		f.setitem(modlist, prog, restart_mode)
		return
	restart_mode = f.findval(modlist, prog)

def do_load(prog, restart_mode):
	if prog == "" or prog == None:
		crt.Screen.Send("\3\r\n#invalid input\r\n")
		crt.Screen.Send("\3\r\n#script terminated for u.\r\n")
		return

	crt.Screen.Send("\3") # ctrl+c; ctrl characters
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
		crt.Screen.Send("\3\r\n#something is wrong, ret "+str(ret)+"\r\n")

restart_mode = "none"  # mode: restart reboot none
modfilename = workdir + "/restart_mode.txt" # must create the file yourself on linux
f = kvfile.kvfile(modfilename)
modlist = f.read()
prog=f.getlastkey(modlist)
prog = crt.Dialog.Prompt("Format: name [,mode]; mode: restart reboot none", "Binary name", str(prog)) # prog = crt.Screen.ReadString({"\r\n","?", "^C"})
if prog != "":
	modeparse(prog, modlist)
	f.write(modlist)
	do_load(prog, restart_mode)
