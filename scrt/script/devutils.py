import time
import log

intr1 = "^C"
intr2 = "<INTERRUPT>"

def wait4pause(crt, time):
	ret = crt.Screen.WaitForStrings([intr1, intr2], time)
	if ret > 0:
		crt.Screen.Send("###user terminated(" + str(ret) + ")!\n")
		return True
	return False

def wait2exec(crt, prompt, timeout, cmd):
	cursec = int(time.time())
	ret = crt.Screen.WaitForStrings([prompt, intr1, intr2], timeout)
	timeinterval = int(time.time()) - cursec
	log.info("wait for prompt " + prompt + " used seconds " + str(timeinterval))
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
		return not wait4pause(crt, 5)
	return False

def is_uboot(crt):
	crt.Screen.Send("\r\n")
	return crt.Screen.WaitForStrings([">>"], 1) == 1

def wait2uboot(crt):
	return is_uboot(crt) or wait2exec(crt, "stop with 'space'", 0xfffffff, " ")

def is_shell(crt):
	crt.Screen.Send("\r\n")
	return crt.Screen.WaitForStrings(["root@SWITCH"], 1) == 1

def try_login(crt):
	crt.Screen.Send("\x1a\x1a\x1a")  # ctrl+z; ctrl characters
	crt.Screen.Send("\r\n")
	if crt.Screen.WaitForStrings(["login"], 1) == 1:  # login needed
		crt.Screen.Send("admin\r\n")
		crt.Screen.WaitForStrings(["Password"], 5)
		crt.Screen.Send("admin\r\n")
		crt.Screen.WaitForStrings([">"], 5)
		crt.Screen.Send("enable\r\n")
		return True
	return False

def cmdreboot(crt): 
	crt.Screen.Send("\x1a\x1a\x1a")  # ctrl+z; ctrl characters
	if not is_shell(crt):
		crt.Screen.Send("entershell\n")
	crt.Screen.Send("reboot\n")
	return True
