import random

timeout = 30
ifarray = ("eth0/7", "eth0/8")

def  shutdown(ifname): 
  crt.Screen.Send("interface " + ifname + "\n")
  crt.Screen.Send("shutdown\n")
  crt.Screen.Send("exit\n")


def  noshutdown(ifname): 
  crt.Screen.Send("interface " + ifname + "\n")
  crt.Screen.Send("no shutdown\n")
  crt.Screen.Send("exit\n")


def  wait4pause(time): 
  return crt.Screen.WaitForStrings(["^C", "<INTERRUPT>", "^Z"], int(time)) #crt.Sleep(10000)


loop = 1
while loop == 1: 
  for (i in ifarray) 
    shutdown(ifarray[i])
    tout = random.randint(0, 120) + 1 # 0 means infinite
    if wait4pause(tout): 
      loop = 0
      break
    
    noshutdown(ifarray[i])
    tout = random.randint(0, 120) + 1 # 0 means infinite
    crt.Screen.Send("#tout " + tout + "\n")
    if wait4pause(tout): 
      loop = 0
      break
    
  

crt.Screen.Send("#script exit\n")
