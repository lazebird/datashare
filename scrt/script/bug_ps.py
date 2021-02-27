import sys
import os
import string
(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import session

sess = session.sess(crt.GetActiveTab())

def	cmdpreconfig(): 
	sess.cmdsexec("end\nentershell\n", clean=False)
	return 1

timeout = 1
count = 0
def	cmdloop(): 
	global count
	count = count + 1
	if "[FAIL] Killing all remaining processes...failed." in sess.get_output(): return False
	# if "Currently running processes (ps)" in sess.get_output(): return False
	if sess.wait(3): return False
	cmdpreconfig()
	sess.cmdexec("find /var/log/ -type f | xargs ls -l \n", clean=False)
	sess.cmdexec("date -s \"2021-02-25 19:55\" && hwclock -w \n", clean=False)
	# sess.cmdexec("/etc/init.d/rc 6 \n")
	sess.cmdexec("reboot \n", clean=False)
	return True

while cmdloop() and sess.cmdreboot() and sess.wait2login("admin", "admin", False):pass
crt.Screen.Send("#game over, count "+str(count)+"!\n")
crt.Dialog.MessageBox("#script exit, count "+str(count))
