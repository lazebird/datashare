import sys, os, random, json

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

from utils import session

defcmdarray = [
    "#multi cmd 1.1\n#multi cmd 1.2",
    "#multi cmd 2.1\n#multi cmd 2.2",
    "#multi cmd 3",
]

sess = session.sess(crt.GetActiveTab())
opts = json.loads(crt.Arguments[0]) if crt.Arguments.Count == 1 else {}
loopnumbase = opts.get("loop", 5)
timeoutbase = opts.get("timeout", 5)
cmdarray = opts.get("cmds", defcmdarray)
reboot = opts.get("reboot", True)
order = opts.get("order", False)


def execcmd(cmdstr):
    crt.Screen.Send(cmdstr + "\n")


def cmdpreconfig():
    crt.Screen.Send("enable\nconfig t\n")
    return 1


def cmdloop(num, timeout):
    cnt = 0
    while cnt < num and not sess.wait(timeout):
        index = (cnt % len(cmdarray)) if order else random.randint(0, len(cmdarray) - 1)
        if "Terminating" in sess.get_output():  # exception when waiting
            return False
        if not sess.cmdsexec(cmdarray[index]):
            return False
        if "Terminating" in sess.get_output():
            return False
        cnt = cnt + 1
    return cnt == num


while True:
    loopcmdnum = loopnumbase + random.randint(0, 9)
    timeout = timeoutbase + random.randint(0, 9)
    crt.Screen.Send("#loopcmdnum " + str(loopcmdnum) + " timeout " + str(timeout) + "\n")
    if not cmdloop(loopcmdnum, timeout):
        break
    if reboot and not (sess.cmdreboot() and sess.wait2login()):
        break
crt.Screen.Send("#game over!\n")
crt.Dialog.MessageBox("#script exit")
