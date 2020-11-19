import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import devutils

loopcmdnum = int(10)
timeout = int(10)
bug_found = False
count = 0

def iobuf_empty():
	devutils.wait4pause(crt, 1)
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
	global count
	iobuf_empty()
	crt.Screen.Send("release\n")
	ret = devutils.wait2exec(crt, ["liulang-deb:"], 1800, "ll release/rootfs.ubi\n")
	if ret != 1:
		return 1
	ret = crt.Screen.WaitForStrings(["151257088"], 3)
	bug_found = (ret != 1)
	count = count + 1
	return bug_found

init_test()
while not bug_check() and not devutils.wait4pause(crt, 3):
	pass
stop_test()
crt.Screen.Send("#Bug Found! Count "+str(count)+"\n" if bug_found else "#Game Over! Count "+str(count)+"\n")
if bug_found:
	crt.Dialog.MessageBox("Bug Found!")
