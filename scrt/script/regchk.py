import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import devutils

loopcmdnum = int(30)
timeout = int(3)
cmdarray=(
	"diagnostic register write 0 0x2040004 ", #0x81700000", 
	"diagnostic register read 0 0x2040150")

def  execcmd(cmdstr):
	crt.Screen.Send(cmdstr+"\n")

def  addZero(str,length):			   
	return (length - str.length + 1).join("0") + str			  

def  cmdloop(num):
	i, data, lastdata
	for (i = 1 i < 20 i+=1) 
		lastdata = 0
		execcmd(cmdarray[0] + "0x8" + addZero(i + "", 2) + "00000")
		crt.Screen.ReadString("SWITCH#", 1)
		j
		for (j = 0 j < 2 j+=1) 
			execcmd(cmdarray[1])
			re = /rv 0 data (\w+)/g
			re1 = /\r*\n/g
			data = crt.Screen.ReadString("SWITCH#", 1)
			data = data.replace(re1, "")
			#crt.Screen.Send("#data "+data+"\n")
			data = re.exec(data)[1]
			crt.Screen.ReadString("SWITCH#", 1)
			if lastdata and lastdata != data: 
				crt.Screen.Send("####################### loop "+i+" data "+data+" lastdata "+lastdata+"#######################\n")
				crt.Screen.ReadString("SWITCH#", 1)
				break
			lastdata = data
			if devutils.wait4pause(crt, 2): 
				return 0
	return 0

#while cmdloop(loopcmdnum) and devutils.cmdreboot(crt) and devutils.wait_login(crt):pass
while cmdloop(loopcmdnum):pass
crt.Screen.Send("#game over!\n")
