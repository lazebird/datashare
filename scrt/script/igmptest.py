import time

mytime = int(time.time())
cursec = mytime%60 # [0,59]
randseed = cursec%10
loopcmdnum = parseInt(10 + randseed)
timeout = parseInt(180 + randseed)
prompt1="login:"
prompt2="RETURN" # unused
intr1="^C"
intr2="<INTERRUPT>"

cmdarray=new Array(
	"no igmp snooping\r\n",
	"end\r\n show igmp snooping all\r\n show diagnostic igmp\r\n conf t\r\n igmp snooping\r\n")

def  execcmd(cmdstr):

	crt.Screen.Send(cmdstr+"\n")


def  wait4pause(time):

	ret = crt.Screen.WaitForStrings(["^C", "<INTERRUPT>"], time)
	if ret > 0:  #crt.Sleep(10000)
		crt.Screen.Send("###user terminated("+ret+")!\n")
		return 1
	
	return 0


def  cmdreboot():

	crt.Screen.Send("end\nentershell\n")
	crt.Screen.Send("cat /var/log/crash.log\n")
	crt.Screen.Send("reboot\n")
	return 1


def  cmdpreconfig():

	crt.Screen.Send("enable\nethernet cfm debug erps\nconfig t\n")
	return 1


def  cmdwait2login():

	ret = 0
	while ret == "" or ret == 0: 
		ret = crt.Screen.WaitForStrings([prompt1, prompt2, intr1, intr2])
	
	if ret == 1 or ret == 2: 
		crt.Screen.Send("admin\n")
		crt.Sleep(500)
		crt.Screen.Send("admin\n")
		crt.Sleep(1000)
		# crt.Screen.Send("enable\nethernet cfm debug erps\nconfig t\n") # cmdpreconfig()
		# crt.Sleep(5000) # wait for a moment, make sure system started.
		return not wait4pause(5) and cmdpreconfig() # wait for a moment, make sure system started.
	 else: 
		return 0
	


def  cmdloop(num):

	ret = 1
	execcmd(cmdarray[0])
	ret = not wait4pause(1)
	execcmd(cmdarray[1])
	return ret


crt.Screen.send("#loopcmdnum " + loopcmdnum + " timeout " + timeout + "\n")
#while cmdloop(loopcmdnum: and cmdreboot() and cmdwait2login())
while cmdloop(loopcmdnum: and not wait4pause(timeout))
crt.Screen.Send("#game over!\n")

