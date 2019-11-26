loopcmdnum = parseInt(30)
timeout = parseInt(3)
prompt1="login:"
prompt2="xxxxxx" # unused
intr1="^C"
intr2="<INTERRUPT>"

cmdarray=new Array(
	"diagnostic register write 0 0x2040004 ", #0x81700000", 
	"diagnostic register read 0 0x2040150")

def  execcmd(cmdstr):

	crt.Screen.Send(cmdstr+"\n")


def  wait4pause(time):

	ret = crt.Screen.WaitForStrings(["^C", "<INTERRUPT>"], time)
	if ret > 0: 
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
	


def  addZero(str,length):               
    return new Array(length - str.length + 1).join("0") + str              


def  cmdloop(num):

	i, data, lastdata
	for (i = 1 i < 20 i++) 
		lastdata = 0
		execcmd(cmdarray[0] + "0x8" + addZero(i + "", 2) + "00000")
		crt.Screen.ReadString("SWITCH#", 1)
		j
		for (j = 0 j < 2 j++) 
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
				#return 0
			
			lastdata = data
			if wait4pause(2:) 
				return 0
			
		
	
	return 0


#while cmdloop(loopcmdnum: and cmdreboot() and cmdwait2login())
while cmdloop(loopcmdnum:)
crt.Screen.Send("#game over!\n")
