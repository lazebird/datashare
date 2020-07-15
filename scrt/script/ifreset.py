import random

timeout = 30
ifarray = {"eth0/1", "eth0/7", "eth0/11"}

def  shutdown(ifname): 
  crt.Screen.Send("interface " + ifname + "\n")
  crt.Screen.Send("shutdown\n")
  crt.Screen.Send("exit\n")


def  noshutdown(ifname): 
  crt.Screen.Send("interface " + ifname + "\n")
  crt.Screen.Send("no shutdown\n")
  crt.Screen.Send("exit\n")


def  wait4pause(time): 
  return crt.Screen.WaitForStrings(["^C", "<INTERRUPT>", "^Z", "failed"], int(time)) #crt.Sleep(10000)


loop = 1
curtabidx = crt.GetActiveTab().Index
while loop == 1: 
  for s in ifarray:
    if curtabidx == 3 and crt.GetActiveTab().Index == 2: # skip when bug occurred
      wait4pause(10)
      continue
    shutdown(s)
    tout = random.randint(0, 120) + 1 # 0 means infinite
    if wait4pause(tout): 
      loop = 0
      break
    if curtabidx == 3 and crt.GetActiveTab().Index == 2: # skip when bug occurred
      wait4pause(10)
      continue
    noshutdown(s)
    tout = random.randint(0, 120) + 1 # 0 means infinite
    crt.Screen.Send("#tout " + str(tout) + "\n")
    if wait4pause(tout): 
      loop = 0
      break

crt.GetScriptTab().Activate()
# crt.Screen.Send("#script exit\n")
crt.Dialog.MessageBox("#script exit")
