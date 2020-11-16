import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)

import fsutils

srvip = "192.168.100.106"#"10.1.1.2"
if crt.Arguments.Count > 0:
    srvip = crt.Arguments[0]

prog = crt.Dialog.Prompt("Please enter binary name; format: name [,mode]; mode: restart reboot none") # prog = crt.Screen.ReadString({"\r\n","?", "^C"})
restart_mode = "none"  # mode: restart reboot none
modhash = {}
modfilename = "D:/restart_mode.txt"

def optparse(s, modhash):
	global prog
	global restart_mode
	s = s.replace("#", ",") # support '#' as ','
	args = s.split(",")
	if len(args) > 1:  # input string has args
		prog = args[0]
		restart_mode = args[1]
		modhash[prog] = restart_mode
	else: 
		if prog in modhash: 
			restart_mode = modhash[prog]

def do_load(prog, restart_mode):
	if prog == "":
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

modhash = eval(fsutils.loadkvfile(modfilename))
optparse(prog, modhash)
fsutils.writekvfile(modfilename, str(modhash))
do_load(prog, restart_mode)
