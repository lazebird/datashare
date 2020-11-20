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
maxcount = 0xfffffff
if crt.Arguments.Count > 0:
	maxcount = int(crt.Arguments[0])


def iobuf_empty():
	sess.wait(1)
	# crt.Session.LogFileName = "/home/liulang/projects/log/session-%S-d%D.log"
	crt.Session.Log(False)
	crt.Session.Log(True)

def init_test():
	crt.Screen.Send("## start\n")

def stop_test():
	crt.Screen.Send("## stop\n")

def do_clean():  # avoid flash full
	return 1

def bug_check():
	global bug_found
	iobuf_empty()
	crt.Screen.Send("release\n")
	ret = sess.wait2exec(["liulang-deb:"], 1800, "ll release/rootfs.ubi\n")
	if ret != 1:
		return 1
	ret = crt.Screen.WaitForStrings(["151257088"], 3)
	bug_found = (ret != 1)
	return bug_found

init_test()
count = 0
while count < maxcount and not bug_check() and not sess.wait(3):
	count = count + 1
stop_test()
crt.Screen.Send("#Bug Found" if bug_found else "#Game Over" + "(count."+str(count)+")!\n")
if bug_found:
	crt.Dialog.MessageBox("Bug Found!")
