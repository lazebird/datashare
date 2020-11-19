import time
import log

intrlist = ["^C", "<INTERRUPT>"]

def wait4pause(crt, time):
	ret = crt.Screen.WaitForStrings(intrlist, time)
	if ret > 0:
		crt.Screen.Send("###user terminated(" + str(ret) + ")!\n")
	return ret # 1/2: on interrupt; 0: on timeout

def wait2exec(crt, promptlist, timeout, cmd):
	cursec = int(time.time())
	plen = len(promptlist)
	promptlist.extend(intrlist)
	ret = crt.Screen.WaitForStrings(promptlist, timeout)
	timeinterval = int(time.time()) - cursec
	log.info("wait for promptlist [" + " ".join(promptlist) + "] used seconds " + str(timeinterval))
	if ret > 0 and ret <= plen:
		crt.Screen.Send(cmd)
	return ret # 1/True: on success; 0: on timeout; 2/3: on interrupt

def wait_login(crt):
	ret = wait2exec(crt, ["login:"], 0xfffffff, "")
	if ret == 1:
		crt.Sleep(5000)
		crt.Screen.Send("admin\n")
		crt.Sleep(1000)
		crt.Screen.Send("admin\n")
		crt.Sleep(3000)
		crt.Screen.Send("enable\nconfig t\n")
		return wait4pause(crt, 5) == 0  # wait for a moment, make sure system started.
	return False

def is_uboot(crt):
	crt.Screen.Send("\r\n")
	return crt.Screen.WaitForStrings([">>"], 1) == 1

def wait2uboot(crt):
	return is_uboot(crt) or wait2exec(crt, ["stop with 'space'"], 0xfffffff, " ") == 1

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
	crt.Screen.Send("\x1a\x1a\x1a\x1a\x1a")  # ctrl+z; ctrl characters
	if not is_shell(crt):
		crt.Screen.Send("entershell\n")
	crt.Screen.Send("reboot\n")
	return True
