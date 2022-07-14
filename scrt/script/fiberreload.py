import sys, os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

from utils import session

sess = session.sess(crt.GetActiveTab())
bug_found = False


def iobuf_empty():
    sess.wait(1)


def do_clean():  # avoid flash full
    crt.Screen.Send("entershell\ncd /var/log\n")
    crt.Screen.Send("rm -rf message syslog kern.log user.log wtmp\n")
    return 1


def bug_check():
    bug_found = crt.Screen.WaitForStrings(["HAL-6: Interface eth0/2"], 3) == 1
    return bug_found


while not bug_check() and do_clean() and sess.cmdreboot() and sess.wait2login():
    pass
crt.Screen.Send("#Bug Found!\n" if bug_found else "#Game Over!\n")
if bug_found:
    crt.Dialog.MessageBox("Bug Found!")
