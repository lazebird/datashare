import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import time
import log
import opt
import session

sess = session.sess(crt.Screen)
opthash = opt.opt(crt.Arguments).tohash()

srvip = "192.168.100.106" # "10.1.1.2"
localip = "" # calc by srvip
if "ip" in opthash:
	srvip = opthash["ip"]

def arg_parse(crt):
	global localip
	cursec = (int(time.time()))%60 # [0,59]
	ip_pending = str(cursec + 190)
	localip = srvip[0:srvip.rindex('.') + 1] + ip_pending # [190,250]

def exec_upgrade(crt):
	if not sess.is_uboot() and not sess.wait2uboot():
		crt.Screen.Send("\3\r\n# script terminated for u.\r\n")
		sys.exit()

	while True:
		crt.Screen.Send("update_rootfs0 " + srvip + " " + localip + " rootfs.ubi\r\n")
		ret = sess.wait2exec(["####"], 20, "")
		if ret > 1:
			crt.Screen.Send("\3\r\n# script terminated for u.\r\n")
			break
		if ret == 0:
			crt.Screen.Send("\3\3\3# retry later\r\n") # ctrl+c to break current update
			crt.Screen.WaitForStrings(["####"], 1) # escape ctrl+c strings
			continue
		ret = sess.wait2exec(["written: OK"], 300, "reset\n")
		if ret > 1:
			crt.Screen.Send("\3\r\n# script terminated for u.\r\n")
		if ret == 0:
			crt.Screen.Send("# fatal error occurred\r\n")
		break

arg_parse(crt)
exec_upgrade(crt)
