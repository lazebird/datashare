loopcmdnum = int(10)
timeout = int(10)
prompt1 = "login:"
prompt2 = "xxxxxx"  # unused
intr1 = "^C"
intr2 = "<INTERRUPT>"
bug_found = False


def iobuf_empty():
    crt.Screen.WaitForStrings(["[should never be read]", intr1, intr2], 1)


def init_test():
    crt.Screen.Send("./guard.sh\n")


def stop_test():
    crt.Screen.Send("./guard.sh stop\n")


def do_clean():  # avoid flash full
    crt.Screen.Send("entershell\ncd /var/log\n")
    crt.Screen.Send("rm -rf message syslog kern.log user.log wtmp\n")
    return 1


def bug_check():
    global bug_found
    iobuf_empty()
    crt.Screen.Send("rm -rf output/*/ && rm -rf output/*.done\n")
    ret = crt.Screen.WaitForStrings(["FAILED"], 1)
    bug_found = (ret == 1)
    crt.Screen.Send("tree output/\n")
    return ret == 1


def wait4pause(time):
    ret = crt.Screen.WaitForStrings(["^C", "<INTERRUPT>"], time)
    if ret > 0:
        # crt.Sleep(10000)
        crt.Screen.Send("###user terminated(" + str(ret) + ")!\n")
        return 1
    return 0


def cmdreboot():
    crt.Screen.Send("end\nentershell\n")
    # crt.Screen.Send("cat /var/log/crash.log\n")
    #   crt.Screen.Send("ls -l /var/core/\n")
    crt.Screen.Send("reboot\n")
    return 1


def cmdwait2login():
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
        # wait for a moment, make sure system started.
        return not wait4pause(30)
    else:
        return 0


init_test()
while not bug_check() and not wait4pause(3):
    pass
stop_test()
crt.Screen.Send("#Bug Found!\n" if bug_found else "#Game Over!\n")
if bug_found:
    crt.Dialog.MessageBox("Bug Found!")
