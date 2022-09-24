import sys, os, json

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

from utils import log

srvip = "2.2.2.106" if crt.GetActiveTab().Caption.find("serial") >= 0 else "192.168.100.106"
workdir = "D:/" if os.path.isdir("D:/") else "/var/lib"

opts = json.loads(crt.Arguments[0]) if crt.Arguments.Count == 1 else {}
srvip = opts.get("ip", srvip)
workdir = opts.get("workdir", workdir)
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


try:
    with open(modfilename) as f:
        conflst = json.load(f)
except:
    conflst = []
prog = len(conflst) and conflst[-1]["name"] or ""
cmd = crt.Dialog.Prompt('Format: NAME, or {"name": "NAME", "mode": {"restart"|"reboot"|"none"}}', "Binary name", str(prog))  # prog = crt.Screen.ReadString({"\r\n","?", "^C"})
cmd = cmd.encode("utf-8").strip()
if len(cmd) > 0:
    try:
        args = json.loads(cmd)
    except:
        args = {}
    name = args.get("name", cmd)
    mode = args.get("mode", (next((x for x in conflst if x["name"] == name), {"mode": "none"}))["mode"] or "none")
    # log.info("conflst=" + str(conflst.get()) + ", cmd[0]=" + cmd[0] + ", cmd[1]=" + str(cmd[1]) + ", mode=" + mode)
    oldobj = len(conflst) and (next((x for x in conflst if x["name"] == name), None))
    oldobj and conflst.remove(oldobj)
    conflst.append({"name": name, "mode": mode})
    with open(modfilename, "w") as f:
        json.dump(conflst, f)
    do_load(name, mode)
