intr1 = "^C"
intr2 = "<INTERRUPT>"

def wait4pause(crt, time):
	ret = crt.Screen.WaitForStrings([intr1, intr2], time)
	if ret > 0:
		crt.Screen.Send("###user terminated(" + str(ret) + ")!\n")
		return True
	return False

def wait2exec(crt, prompt, time, cmd):
	ret = crt.Screen.WaitForStrings([prompt, intr1, intr2], time)
	if ret == 1:
		crt.Screen.Send(cmd)
		return True
	return False

def wait_login(crt):
	ret = wait2exec(crt, "login:", 0xfffffff, "")
	if ret == 1:
		crt.Sleep(5000)
		crt.Screen.Send("admin\n")
		crt.Sleep(1000)
		crt.Screen.Send("admin\n")
		crt.Sleep(3000)
		crt.Screen.Send("enable\nconfig t\n")
		# wait for a moment, make sure system started.
		return not wait4pause(5)
	return False

def wait2uboot(crt):
	return wait2exec(crt, "stop with 'space'", 0xfffffff, " ")

def try_login(crt):
	crt.Screen.Send("\x1a\x1a\x1a")  # ctrl+z; ctrl characters
	crt.Screen.Send("\r\n")
	ret = crt.Screen.WaitForStrings(["login"], 1)
	if ret == 1:  # login needed
		crt.Screen.Send("admin\r\n")
		crt.Screen.WaitForStrings(["Password"], 3)
		crt.Screen.Send("admin\r\n")
		crt.Screen.WaitForStrings([">"], 3)
		crt.Screen.Send("enable\r\n")
	return ret == 1

def cmdreboot(crt): 
  crt.Screen.Send("end\nentershell\n")
  crt.Screen.Send("reboot\n")
  return True
