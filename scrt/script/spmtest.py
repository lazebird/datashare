loopcmdnum = parseInt(30)
timeout = parseInt(5)
prompt1="login:"
prompt2="xxxxxx" # unused
intr1="^C"
intr2="<INTERRUPT>"

cmdarray=new Array(
	"spanning-tree mode rstp", 
	"spanning-tree mode stp", 
	"spanning-tree mode provider-rstp edge", 
	"spanning-tree mode mstp", 
	"end\r\nshow vlan all\r\n \r\n \r\n \r\n \r\n \r\n \r\nconf t", 
	"vlan 2-10 type service point", 
	"vlan 2-10", 
	"spanning-tree enable", 
	"igmp snooping")

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


def  cmdwait2login():

	ret = 0
	while ret == "" or ret == 0: 
		ret = crt.Screen.WaitForStrings([prompt1, prompt2, intr1, intr2])
	
	if ret == 1 or ret == 2: 
		crt.Screen.Send("admin\n")
		crt.Sleep(500)
		crt.Screen.Send("admin\n")
		crt.Sleep(1000)
		crt.Screen.Send("enable\nconfig t\n")
		# crt.Sleep(5000) # wait for a moment, make sure system started.
		return not wait4pause(5) # wait for a moment, make sure system started.
	 else: 
		return 0
	


def  cmdloop(num):

	#crt.Screen.Send("logging level nsm 7\nlogging console 7\n")
	while num-- and not wait4pause(timeout:) 
		execcmd(cmdarray[Math.floor(Math.random()*cmdarray.length)])
	
	return (num == -1)


#while cmdloop(loopcmdnum: and cmdreboot() and cmdwait2login())
while cmdloop(loopcmdnum:)
crt.Screen.Send("#game over!\n")

