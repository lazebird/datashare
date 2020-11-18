import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import devutils
import random

loopcmdnum = int(4)
timeout = int(100)

cmdarray=(
	"interface eth0/1\r\n shutdown\r\nexit",
	"interface eth0/1\r\n no shutdown\r\nexit",
	"interface eth0/10\r\n shutdown\r\nexit",
	"interface eth0/10\r\n no shutdown\r\nexit"
	)

def	 execcmd(cmdstr):
	#crt.Screen.Send("#"+cmdstr+"\n")
	crt.Screen.Send("#fake command\n")

def	 cmdloop(num):
	#crt.Screen.Send("logging level nsm 7\nlogging console 7\n")
	while num>0 and not devutils.wait4pause(crt, timeout):
		num = num - 1 
		execcmd(cmdarray[random.randint(0,len(cmdarray) - 1)])
	return (num == 0)

while cmdloop(loopcmdnum) and devutils.cmdreboot(crt) and devutils.wait_login(crt):pass
crt.Screen.Send("#game over!\n")
