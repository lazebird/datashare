import sys, os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

from utils import session

sess = session.sess(crt.GetActiveTab())
loopcmdnum = int(10)
timeout = int(10)
bug_found = False


def iobuf_empty():
    sess.wait(1)
    # crt.Session.LogFileName = "/home/liulang/projects/log/session-%S-d%D.log"
    crt.Session.Log(False)
    crt.Session.Log(True)


def init_test():
    crt.Screen.Send("## start\n")


def stop_test():
    crt.Screen.Send("## stop\n")


def do_clean():  # avoid flash full
    crt.Screen.Send("entershell\ncd /var/log\n")
    crt.Screen.Send("rm -rf message syslog kern.log user.log wtmp\n")
    return 1


def bug_check():
    global bug_found
    iobuf_empty()
    crt.Screen.Send("make distclean && time make all V=1 -j12\n")
    # crt.Screen.Send("make distclean && make dep V=1 -j12 && time make all V=1 -j12\n")
    # crt.Screen.Send("rm -f dep/hsl.dep && make dep-lib-hsl -j12 && make liba-hsl -j12\n")
    ret = crt.Screen.WaitForStrings([" Error ", "liulang-deb:"], 300)
    bug_found = ret == 1
    if bug_found:
        return True
    crt.Screen.Send("du -hd 0 bin/\n")
    ret = crt.Screen.WaitForStrings(["89M"], 3)
    bug_found = ret != 1
    return ret != 1


init_test()
while not bug_check() and not sess.wait(3):
    pass
stop_test()
crt.Screen.Send("#Bug Found!\n" if bug_found else "#Game Over!\n")
if bug_found:
    crt.Dialog.MessageBox("Bug Found!")
