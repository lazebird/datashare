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

def gen_cmd():
	s = ""
	for num in range(random.randint(1, 40)):
		s = s+str(gen_ch())
	return "echo \""+s+"\" >> \"abc.txt\""

def	cmdpreconfig(): 
	crt.Screen.Send("end\nentershell\n")
	return 1

timeout = 1
def	cmdloop(): 
	cmdpreconfig()
	while True: #not sess.wait(timeout):
		if not sess.cmdsexec(gen_cmd()): return False
		if "^C" in sess.get_output(): return False
		if "No space left on device" in sess.get_output(): break
	return True

while cmdloop() and sess.cmdreboot() and sess.wait2login("admin", "abc"):pass
crt.Screen.Send("#game over!\n")
crt.Dialog.MessageBox("#script exit")
