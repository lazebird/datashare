import time
import log

class sess:
	def __init__(self, crt):
		self.crt = crt
		self.intrlist = ["^C", "<INTERRUPT>"]
		self.output = None
		self.ret = None
	
	def add_intr(self, intrlist):
		self.intrlist.extend(intrlist)
	
	def get_intrlist(self):
		return self.intrlist
	
	def get_output(self):
		return self.output
	
	def get_ret(self):
		return self.ret

	def wait(self, timeout):
		self.output = self.crt.Screen.ReadString(self.intrlist, timeout)
		self.ret = self.crt.Screen.MatchIndex
		if self.ret > 0:
			self.crt.Screen.Send("###user terminated(" + str(self.ret) + ")!\n")
		return self.ret # 1/2: on interrupt; 0: on timeout; securecrt donot support tuple(ret, output) return, or else output can be used to check for other exceptions!

	def wait2exec(self, promptlist, timeout, cmd):
		cursec = int(time.time())
		plen = len(promptlist)
		promptlist.extend(self.intrlist)
		self.output = self.crt.Screen.ReadString(promptlist, timeout)
		self.ret = self.crt.Screen.MatchIndex
		timeinterval = int(time.time()) - cursec
		log.info("wait for promptlist [" + " ".join(promptlist) + "] used seconds " + str(timeinterval))
		if self.ret > 0 and self.ret <= plen:
			self.crt.Screen.Send(cmd)
		return self.ret # 1/True: on success; 0: on timeout; 2/3: on interrupt

	def wait2login(self):
		ret = self.wait2exec(["login:"], 0xfffffff, "")
		if ret == 1:
			self.crt.Sleep(5000)
			self.crt.Screen.Send("admin\n")
			self.crt.Sleep(1000)
			self.crt.Screen.Send("admin\n")
			self.crt.Sleep(3000)
			self.crt.Screen.Send("enable\nconfig t\n")
			return self.wait(5) == 0  # wait for a moment, make sure system started.
		return False

	def is_uboot(self):
		self.crt.Screen.Send("\r\n")
		return self.crt.Screen.WaitForStrings([">>"], 1) == 1

	def wait2uboot(self):
		return self.wait2exec(["stop with 'space'"], 0xfffffff, " ") == 1

	def is_shell(self):
		self.crt.Screen.Send("\r\n")
		return self.crt.Screen.WaitForStrings(["root@SWITCH"], 1) == 1

	def try_login(self, uname="admin", passwd="admin"):
		self.crt.Screen.Send("\x1a\x1a\x1a")  # ctrl+z; ctrl characters
		self.crt.Screen.Send("\r\n")
		if self.crt.Screen.WaitForStrings(["login"], 1) == 1:  # login needed
			self.crt.Screen.Send(uname + "\r\n")
			self.crt.Screen.WaitForStrings(["Password"], 5)
			self.crt.Screen.Send(passwd + "\r\n")
			self.crt.Screen.WaitForStrings([">"], 5)
			self.crt.Screen.Send("enable\r\n")
			return True
		return False

	def cmdreboot(self): 
		self.crt.Screen.Send("\x1a\x1a\x1a")  # ctrl+z; ctrl characters
		if not self.is_shell():
			self.crt.Screen.Send("\x1a\x1a\x1a")  # ctrl+z; ctrl characters
			self.crt.Screen.Send("\nentershell\n")
		self.crt.Screen.Send("reboot\n")
		return True
