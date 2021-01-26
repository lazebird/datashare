import sys
import os
import string
import random
(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import session

sess = session.sess(crt.GetActiveTab())

def gen_ch():
	return random.choice(string.ascii_letters + string.digits)

def gen_cmd(len, target):
	s = ""
	for num in range(len):
		s = s+str(gen_ch())
	return "echo \""+s+"\" >> "+ target

def gen_file(len, target):
	if not sess.cmdsexec("echo > "+target, clean=True): return False
	for i in range(len/40): 
		if not sess.cmdsexec(gen_cmd(40, target), clean=False): return False
	if not sess.cmdsexec(gen_cmd(len%40, target), clean=False): return False

def dump_file(src, target):
	if not sess.cmdsexec("cat "+src+" >> "+target, clean=False): return False
	if "^C" in sess.get_output(): return False
	if "No space left on device" in sess.get_output(): return False
	return True

def	cmdpreconfig(): 
	crt.Screen.Send("end\nentershell\n")
	return 1

timeout = 1
def	cmdloop(): 
	cmdpreconfig()
	gen_file(1024, "1k.txt")
	while True: #not sess.wait(timeout):
		if not dump_file("1k.txt", "abc.txt"): break
	while True: #not sess.wait(timeout):
		if not sess.cmdsexec(gen_cmd(random.randint(1, 40), "abc.txt"), clean=False): return False
		if "^C" in sess.get_output(): return False
		if "No space left on device" in sess.get_output(): break
	return True

while cmdloop() and sess.cmdreboot() and sess.wait2login("admin", "abc"):pass
crt.Screen.Send("#game over!\n")
crt.Dialog.MessageBox("#script exit")
