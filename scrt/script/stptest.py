loopcmdnum = 5 + Math.floor(Math.random() * 10)
timeout = 5 + Math.floor(Math.random() * 10)
prompt1 = "login:"
prompt2 = "RETURN" # unused
intr1 = "^C"
intr2 = "<INTERRUPT>"

cmdarray = new Array(
  "interface eth0/7\r\nshutdown\r\nexit",
  "interface eth0/7\r\nno shutdown\r\nexit",
  "interface eth0/8\r\nshutdown\r\nexit",
  "interface eth0/8\r\nno shutdown\r\nexit"
)

def  execcmd(cmdstr): 
  crt.Screen.Send(cmdstr + "\n")


def  wait4pause(time): 
  ret = crt.Screen.WaitForStrings(["^C", "<INTERRUPT>"], time)
  if ret > 0: 
    crt.Screen.Send("###user terminated(" + ret + ")!\n")
    return 1
  
  return 0


def  cmdreboot(): 
  crt.Screen.Send("end\nentershell\n")
  crt.Screen.Send("reboot\n")
  return 1


def  cmdpreconfig(): 
  crt.Screen.Send("enable\nconfig t\n")
  return 1


def  cmdwait2login(): 
  ret = crt.Screen.WaitForStrings([prompt1, prompt2, intr1, intr2])
  if ret == 1 or ret == 2: 
    crt.Screen.Send("admin\n")
    crt.Sleep(500)
    crt.Screen.Send("admin\n")
    crt.Sleep(1000)
    return not wait4pause(5) and cmdpreconfig() # wait for a moment, make sure system started.
   else: 
    return 0
  


def  cmdloop(num): 
  while num-- and not wait4pause(timeout:) 
    execcmd(cmdarray[Math.floor(Math.random() * cmdarray.length)])
  
  return num == -1


crt.Screen.send("#loopcmdnum " + loopcmdnum + " timeout " + timeout + "\n")
while cmdloop(loopcmdnum: and cmdreboot() and cmdwait2login())
crt.Screen.Send("#game over!\n")
