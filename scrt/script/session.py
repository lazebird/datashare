import time
import log

class sess:
	def __init__(self, tab):
		self.screen = tab.Screen
		self.name = tab.Caption
		self.intrlist = ["^C", "<INTERRUPT>"]
		self.output = ""
		self.ret = 0
		self.errmsg = ""
		self.screen.Synchronous = True
		log.info(self.name + ": init session")
	
	def add_intr(self, intrlist):
		self.intrlist.extend(intrlist)
	
	def get_intrlist(self):
		return self.intrlist
	
	def get_output(self):
		return self.output
	
	def get_ret(self):
		return self.ret

	def get_errmsg(self):
		return self.errmsg

	def read(self, promptlist, timeout):
		output = self.screen.ReadString(promptlist, timeout)
		self.ret = self.screen.MatchIndex
		if len(output) > 0:
			self.output = output

	def wait(self, timeout):
		self.read(self.intrlist, timeout)
		if self.ret > 0:
			self.errmsg = "###user terminated(" + str(self.ret) + ")!"
			self.screen.Send(self.errmsg+"\n")
		return self.ret # 1/2: on interrupt; 0: on timeout; securecrt donot support tuple(ret, output) return, or else output can be used to check for other exceptions!

	def wait2exec(self, promptlist, timeout, cmd):
		cursec = int(time.time())
		plen = len(promptlist)
		promptlist.extend(self.intrlist)
		self.read(promptlist, timeout)
		timeinterval = int(time.time()) - cursec
		log.info(self.name + ": " + "wait for promptlist [" + " ".join(promptlist) + "] used seconds " + str(timeinterval))
		if self.ret > 0 and self.ret <= plen:
			self.screen.Send(cmd)
		return self.ret # 1/True: on success; 0: on timeout; 2/3: on interrupt

	def wait2login(self):
		ret = self.wait2exec(["login:"], 0xfffffff, "")
		if ret == 1:
			time.sleep(5)
			self.screen.Send("admin\n")
			time.sleep(1)
			self.screen.Send("admin\n")
			time.sleep(3)
			self.screen.Send("enable\nconfig t\n")
			return self.wait(5) == 0  # wait for a moment, make sure system started.
		return False

	def is_uboot(self):
		self.screen.Send("\r\n")
		return self.screen.WaitForStrings([">>"], 1) == 1

	def wait2uboot(self):
		return self.wait2exec(["stop with 'space'"], 0xfffffff, " ") == 1

	def is_shell(self):
		self.screen.Send("\r\n")
		return self.screen.WaitForStrings(["root@SWITCH"], 1) == 1

	def try_login(self, uname="admin", passwd="admin"):
		self.screen.Send("\x1a\x1a\x1a")  # ctrl+z; ctrl characters
		self.screen.Send("\r\n")
		if self.screen.WaitForStrings(["login"], 1) == 1:  # login needed
			self.screen.Send(uname + "\r\n")
			self.screen.WaitForStrings(["Password"], 5)
			self.screen.Send(passwd + "\r\n")
			self.screen.WaitForStrings([">"], 5)
			self.screen.Send("enable\r\n")
			return True
		return False

	def cmdreboot(self): 
		self.screen.Send("\x1a\x1a\x1a")  # ctrl+z; ctrl characters
		if not self.is_shell():
			self.screen.Send("\x1a\x1a\x1a")  # ctrl+z; ctrl characters
			self.screen.Send("\nentershell\n")
		self.screen.Send("reboot\n")
		return True

	# cmd send by crt may be later than send() called? there should be enough time to wait, if timeout, script fail; else no time will be wasted
	def cmdexec(self, cmdstr, prompt="SWITCH", timeout=9): 
		self.screen.WaitForStrings(["should never be matched"], 1) # clear screen buffer
		fcmdstr = cmdstr + "\n"
		self.screen.Send(fcmdstr)
		if self.screen.WaitForStrings([cmdstr], timeout) != 1: # wait for echo
			self.errmsg = "cmd "+cmdstr+" echo failed"
			log.err(self.name + ": errmsg " + self.errmsg)
			return False
		self.read([prompt], timeout)
		if self.ret != 1:
			self.errmsg = "cmd "+cmdstr+" prompt "+prompt+" wait failed"
			log.err(self.name + ": ret " + str(self.ret) + ", errmsg " + self.errmsg + ", output " + self.output )
			return False
		return True

	def cmdsexec(self, cmdsstr, prompt="SWITCH", timeout=9): 
		cmdsstr = cmdsstr.replace("\r", "")
		cmds = cmdsstr.split("\n")
		for cmdstr in cmds:
			if not self.cmdexec(cmdstr, prompt, timeout):
				return False
		return True
