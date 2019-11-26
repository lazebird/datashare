# 测试vrrp重启后实例未就绪问题
loopcmdnum = parseInt(10)
timeout = parseInt(10)
prompt1 = "login:"
prompt2 = "xxxxxx" # unused
intr1 = "^C"
intr2 = "<INTERRUPT>"
bug_found = false

def  iobuf_empty(): 
  crt.Screen.WaitForStrings(["[should never be read]", intr1, intr2], 1)


def  init_debug(): 
  crt.Screen.Send("entershell\n")
  crt.Screen.Send("sed -i 's/vrrpd.*/vrrpd -d -D all/'  /etc/init.d/zebos\n")
  crt.Screen.Send("exit\n")

# avoid flash full
def  do_clean(): 
  crt.Screen.Send("entershell\ncd /var/log\n")
  crt.Screen.Send("rm -rf message syslog kern.log user.log wtmp\n")
  return 1

def  bug_check(): 
  iobuf_empty()
  crt.Screen.Send("show vrrp | include State\n")
  ret = crt.Screen.WaitForStrings(["Initialize", "SWITCH#"], timeout)
  bug_found = ret == 1
  return ret == 1


def  wait4pause(time): 
  ret = crt.Screen.WaitForStrings(["^C", "<INTERRUPT>"], time)
  if ret > 0: 
    #crt.Sleep(10000)
    crt.Screen.Send("###user terminated(" + ret + ")!\n")
    return 1
  
  return 0


def  cmdreboot(): 
  crt.Screen.Send("end\nentershell\n")
  # crt.Screen.Send("cat /var/log/crash.log\n")
  #   crt.Screen.Send("ls -l /var/core/\n")
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
    crt.Screen.Send("enable\n")
    # crt.Sleep(5000) # wait for a moment, make sure system started.
    return not wait4pause(30) # wait for a moment, make sure system started.
   else: 
    return 0
  


init_debug()
while not bug_check(: and do_clean() and cmdreboot() and cmdwait2login())
#while not wait4pause(300: and cmdreboot() and cmdwait2login())
crt.Screen.Send("#Bug Found!\n" if bug_found else "#Game Over!\n")
if bug_found: crt.Dialog.MessageBox("Bug Found!")
