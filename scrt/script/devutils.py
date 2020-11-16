intr1 = "^C"
intr2 = "<INTERRUPT>"

def  wait4pause(time): 
  ret = crt.Screen.WaitForStrings([intr1, intr2], time)
  if ret > 0: 
    crt.Screen.Send("###user terminated(" + str(ret) + ")!\n")
    return 1
  return 0

def wait2exec(prompt, time, cmd):
  ret = crt.Screen.WaitForStrings([prompt, intr1, intr2], time)
  if ret == 1: 
    crt.Screen.Send(cmd)
    return 1
  return 0

def  wait_login(): 
	ret = wait2exec("login:", 0xfffffff, "")
	if ret == 1:
		crt.Sleep(5000)
		crt.Screen.Send("admin\n")
		crt.Sleep(1000)
		crt.Screen.Send("admin\n")
		crt.Sleep(3000)
		crt.Screen.Send("enable\nconfig t\n")
		return not wait4pause(5) # wait for a moment, make sure system started.
	return 0

def wait2uboot():
	return wait2exec("stop with 'space'", 0xfffffff, " ")
