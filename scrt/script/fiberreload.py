import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import devutils

bug_found = False

def iobuf_empty():
	devutils.wait4pause(crt, 1)

def do_clean():  # avoid flash full
	crt.Screen.Send("entershell\ncd /var/log\n")
	crt.Screen.Send("rm -rf message syslog kern.log user.log wtmp\n")
	return 1

def bug_check():
	return bug_found = crt.Screen.WaitForStrings(["HAL-6: Interface eth0/2"], 3) == 1

while not bug_check() and do_clean() and devutils.cmdreboot(crt) and devutils.wait_login(crt):
	pass
#while not devutils.wait4pause(crt, 300) and devutils.cmdreboot(crt) and devutils.wait_login(crt):pass
crt.Screen.Send("#Bug Found!\n" if bug_found else "#Game Over!\n")
if bug_found:
	crt.Dialog.MessageBox("Bug Found!")
