import random

loopcmdnum = int(4)
timeout = int(100)
prompt1="login:"
prompt2="xxxxxx" # unused
intr1="^C"
intr2="<INTERRUPT>"

cmdarray=(
	"interface eth0/1\r\n shutdown\r\nexit",
	"interface eth0/1\r\n no shutdown\r\nexit",
	"interface eth0/10\r\n shutdown\r\nexit",
	"interface eth0/10\r\n no shutdown\r\nexit"
	)

def	 execcmd(cmdstr):

	#crt.Screen.Send("#"+cmdstr+"\n")
	crt.Screen.Send("#fake command\n")


def	 wait4pause(time):

	ret = crt.Screen.WaitForStrings(["^C", "<INTERRUPT>"], time)
	if ret > 0:	 #crt.Sleep(10000)
		crt.Screen.Send("###user terminated("+ret+")!\n")
		return 1
	
	return 0


def	 cmdreboot():

	crt.Screen.Send("end\nentershell\n")
	# crt.Screen.Send("cat /var/log/crash.log\n")
	crt.Screen.Send("ls -l /var/core/\n")
	crt.Screen.Send("reboot\n")
	return 1


def	 cmdwait2login():

	ret = 0
	while ret == "" or ret == 0: 
		ret = crt.Screen.WaitForStrings([prompt1, prompt2, intr1, intr2])
	
	if ret == 1 or ret == 2: 
		crt.Sleep(5000)
		crt.Screen.Send("admin\n")
		crt.Sleep(1000)
		crt.Screen.Send("admin\n")
		crt.Sleep(3000)
		crt.Screen.Send("enable\nconfig t\n")
		# crt.Sleep(5000) # wait for a moment, make sure system started.
		return not wait4pause(5) # wait for a moment, make sure system started.
	else: 
		return 0
	


def	 cmdloop(num):

	#crt.Screen.Send("logging level nsm 7\nlogging console 7\n")
	while num>0 and not wait4pause(timeout):
		num-=1 
		execcmd(cmdarray[random.randint(0,len(cmdarray) - 1)])
	
	return (num == 0)


while cmdloop(loopcmdnum) and cmdreboot() and cmdwait2login():pass
#while not wait4pause(300) and cmdreboot() and cmdwait2login():pass
crt.Screen.Send("#game over!\n")

