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
	crt.Screen.Send("./guard.sh\n")

def stop_test():
	crt.Screen.Send("./guard.sh stop\n")


def do_clean():  # avoid flash full
	crt.Screen.Send("entershell\ncd /var/log\n")
	crt.Screen.Send("rm -rf message syslog kern.log user.log wtmp\n")
	return 1

def bug_check():
	global bug_found
	iobuf_empty()
	crt.Screen.Send("rm -rf output/*/ && rm -rf output/*.done\n")
	ret = crt.Screen.WaitForStrings(["FAILED"], 1)
	bug_found = (ret == 1)
	crt.Screen.Send("tree output/\n")
	return ret == 1

init_test()
while not bug_check() and not sess.wait(3):
	pass
stop_test()
crt.Screen.Send("#Bug Found!\n" if bug_found else "#Game Over!\n")
if bug_found:
	crt.Dialog.MessageBox("Bug Found!")
