import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import devutils
import stringutils
import time
import log

srvip = "192.168.100.106" # "10.1.1.2"
localip = "" # calc by srvip

def arg_parse(crt):
	global srvip
	global localip
	workdir = "D:/"
	argstr = ""
	for index in range(crt.Arguments.Count):
		argstr = argstr + crt.Arguments[index] + " "

	optstr = stringutils.optparse(argstr)
	opthash = eval(optstr)
	if "ip" in opthash:
		srvip = opthash["ip"]
	if "workdir" in opthash:
		workdir = opthash["workdir"]
	log.init(workdir)
	cursec = (int(time.time()))%60 # [0,59]
	ip_pending = str(cursec + 190)
	localip = srvip[0:srvip.rindex('.') + 1] + ip_pending # [190,250]

def exec_upgrade(crt):
	if not devutils.wait2uboot(crt):
		crt.Screen.Send("\3\r\n# script terminated for u.\r\n")
		sys.exit()

	while True:
		crt.Screen.Send("update_rootfs0 " + srvip + " " + localip + " rootfs.ubi\r\n")
		ret = devutils.wait2exec(crt, "####", 20, "")
		if ret > 1:
			crt.Screen.Send("\3\r\n# script terminated for u.\r\n")
			break
		if ret == 0:
			crt.Screen.Send("\3\3\3# retry later\r\n") # ctrl+c to break current update
			crt.Screen.WaitForStrings(["####"], 1) # escape ctrl+c strings
			continue
		ret = devutils.wait2exec(crt, "written: OK", 300, "reset\n")
		if ret > 1:
			crt.Screen.Send("\3\r\n# script terminated for u.\r\n")
		if ret == 0:
			crt.Screen.Send("# fatal error occurred\r\n")
		break

arg_parse(crt)
exec_upgrade(crt)
