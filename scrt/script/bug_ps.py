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
	sess.cmdsexec("end\nentershell", clean=False)
	return 1

timeout = 1
count = 0
cause = "unknown"
def	cmdloop(): 
	global count
	global cause
	count = count + 1
	if "ps -ef" in sess.get_output(): # "[FAIL] Killing all remaining processes...failed." always occurs invalid charactors
		cause = "error detect"
		return False
	# if "Currently running processes (ps)" in sess.get_output(): return False
	if sess.wait(3): 
		cause = "user interrupt"
		return False
	cmdpreconfig()
	sess.cmdexec("find /var/log/ -type f | xargs ls -l", clean=False)
	if not "10001" in sess.name :sess.cmdexec("date -s \"2021-02-25 19:55\" && hwclock -w", clean=False)
	# sess.cmdexec("/etc/init.d/rc 6 \n")
	# sess.cmdexec("reboot", clean=False)
	return True

while cmdloop() and sess.cmdreboot() and sess.wait2login("admin", "admin", False):pass
errmsg = "#"+sess.name+" game over, count "+str(count)+", cause "+cause+"!"
if cause == "unknown": # dump stacks
	crt.Screen.SendSpecial("TN_BREAK")
	crt.Screen.Send("l") # Shows a stack backtrace for all active CPUs.	
	crt.Sleep(1)
	crt.Screen.SendSpecial("TN_BREAK")
	crt.Screen.Send("t") # Output a list of current tasks and their information to the console	
crt.Screen.Send(errmsg+"\n")
crt.Dialog.MessageBox(errmsg)
