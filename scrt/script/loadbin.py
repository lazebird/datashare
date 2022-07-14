import sys, os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

from utils import opt, kvlist, log, file

opts = opt.opt(crt.Arguments)

srvip = "2.2.2.106" if crt.GetActiveTab().Caption.find("serial") >= 0 else "192.168.100.106"
srvip = opts.getval("ip") or srvip

workdir = "D:/" if os.path.isdir("D:/") else "/var/lib"
workdir = opts.getval("workdir") or workdir
modfilename = workdir + "/restart_mode.txt"  # must create the file yourself on linux


def do_load(prog, restart_mode):
    if prog == "" or prog == None:
        crt.Screen.Send("\3\r\n#invalid input\r\n")
        crt.Screen.Send("\3\r\n#script terminated for u.\r\n")
        return

    crt.Screen.Send("\3")  # ctrl+c; ctrl characters
    crt.Screen.WaitForString("root", 1)
    crt.Screen.Send("wget http://" + srvip + "/bin/" + prog + "\r\n")
    ret = crt.Screen.WaitForStrings(["saved", "100%", "failed", "ERROR", "No such", "^C"])
    if ret == 1 or ret == 2:
        crt.Screen.Send("chmod 777 " + prog + " && mv /usr/bin/" + prog + " /" + prog + ".bak && mv " + prog + " /usr/bin && sync\r\n")
        crt.Screen.WaitForStrings(["root", "#", "^C"])
        if restart_mode == "restart":
            crt.Screen.Send("pkill " + prog + "\r\n")
            crt.Screen.WaitForString("root", 1)
            crt.Screen.Send(prog + " &\r\n")
        elif restart_mode == "reboot":
            crt.Screen.Send("reboot\r\n")
        elif restart_mode == "none":
            crt.Screen.Send("\3\r\n#please deal with it ASAP.\r\n")
    else:
        crt.Screen.Send("\3\r\n#something is wrong, ret " + str(ret) + "\r\n")


conf = kvlist.kvlist(file.read(modfilename))
prog = conf.lastkey() or ""
prog = crt.Dialog.Prompt("Format: name [,mode]; mode: restart reboot none", "Binary name", str(prog))  # prog = crt.Screen.ReadString({"\r\n","?", "^C"})
prog = prog.encode("utf-8").strip()
if len(prog) > 0:
    cmd = (opt.parse(prog)).items()[0]
    mode = (cmd[1] == True and conf.findval(cmd[0]) or "none") or cmd[1]  # mode: restart reboot none
    conf.add(cmd[0], mode)
    file.write(modfilename, str(conf.get()) + "\n")
    do_load(cmd[0], mode)
