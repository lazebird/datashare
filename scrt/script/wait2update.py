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

srvip = "192.168.100.106"#"10.1.1.2"
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

if devutils.wait2uboot(crt):
	crt.Screen.Send("update_rootfs0 " + srvip + " " + localip + " rootfs.ubi\r\n")
	if not devutils.wait2exec(crt, "##", 15, ""):
		crt.Screen.Send("\3\3\3")
		crt.Screen.Send("#err\r\n")
	elif not devutils.wait2exec(crt, "written: OK", 300, "reset\n"):
		crt.Screen.Send("#err\r\n")
