import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import session

sess = session.sess(crt)
loopcmdnum = int(10)
timeout = int(10)
bug_found = False

def iobuf_empty():
	sess.wait(1)

def init_test():
	crt.Screen.Send("entershell\n")
	crt.Screen.Send("sed -i 's/vrrpd.*/vrrpd -d -D all/' /etc/init.d/zebos\n")
	crt.Screen.Send("exit\n")

def stop_test():
	crt.Screen.Send("entershell\n")
	crt.Screen.Send("sed -i 's/vrrpd -d -D all/vrrpd -d/' /etc/init.d/zebos\n")
	crt.Screen.Send("exit\n")

def do_clean():  # avoid flash full
	crt.Screen.Send("entershell\ncd /var/log\n")
	crt.Screen.Send("rm -rf message syslog kern.log user.log wtmp\n")
	return 1

def bug_check():
	iobuf_empty()
	crt.Screen.Send("show vrrp | include State\n")
	return bug_found = crt.Screen.WaitForStrings(["Initialize", "SWITCH#"], timeout) == 1

init_test()
while not bug_check() and do_clean() and sess.cmdreboot() and sess.wait2login():
	pass
stop_test()
crt.Screen.Send("#Bug Found!\n" if bug_found else "#Game Over!\n")
if bug_found:
	crt.Dialog.MessageBox("Bug Found!")
