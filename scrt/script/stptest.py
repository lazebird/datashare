import sys
import os
import random

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import session

sess = session.sess(crt.GetActiveTab())
loopcmdnum = 5 + random.randint(0,9)
timeout = 5 + random.randint(0,9)
cmdarray = (
	"interface eth0/25\r\nshutdown\r\nexit",
	"interface eth0/25\r\nno shutdown\r\nexit",
	"interface eth0/26\r\nshutdown\r\nexit",
	"interface eth0/26\r\nno shutdown\r\nexit",
	"interface eth0/27\r\nshutdown\r\nexit",
	"interface eth0/27\r\nno shutdown\r\nexit",
	"interface eth0/28\r\nshutdown\r\nexit",
	"interface eth0/28\r\nno shutdown\r\nexit"
)

def	execcmd(cmdstr): 
	crt.Screen.Send(cmdstr + "\n")

def	cmdpreconfig(): 
	crt.Screen.Send("enable\nconfig t\n")
	return 1

def	cmdloop(num): 
	while num>0 and not sess.wait(timeout):
		num = num - 1
		if "Terminating" in sess.get_output(): # exception when waiting
			return False
		if not sess.cmdsexec(cmdarray[random.randint(0,len(cmdarray) - 1)]):
			return False
		if "Terminating" in sess.get_output():
			return False
	return (num == 0)

crt.Screen.Send("#loopcmdnum " + str(loopcmdnum) + " timeout " + str(timeout) + "\n")
while cmdloop(loopcmdnum) and sess.cmdreboot() and sess.wait2login():pass
crt.Screen.Send("#game over!\n")
