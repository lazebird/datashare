import sys, os, time

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

from utils import opt, session

sess = session.sess(crt.GetActiveTab())
opts = opt.opt(crt.Arguments)

srvip = "2.2.2.106" if crt.GetActiveTab().Caption.find("serial") >= 0 else "192.168.100.106"
srvip = opts.getval("ip") or srvip
localip = ""  # calc by srvip


def genLip(crt):
    global localip
    cursec = (int(time.time())) % 60  # [0,59]
    ip_pending = str(cursec + 190)
    localip = srvip[0 : srvip.rindex(".") + 1] + ip_pending  # [190,250]


def exec_upgrade(crt):
    loop = True
    if not sess.is_uboot() and not sess.wait2uboot():
        crt.Screen.Send("\3\r\n# script terminated for u.\r\n")
        loop = False

    while loop:
        crt.Screen.Send("update_rootfs0 " + srvip + " " + localip + " rootfs.ubi\r\n")
        ret = sess.wait2exec(["####"], 20, "")
        if ret > 1:
            crt.Screen.Send("\3\r\n# script terminated for u.\r\n")
            break
        if ret == 0:
            crt.Screen.Send("\3\3\3# retry later\r\n")  # ctrl+c to break current update
            crt.Screen.WaitForStrings(["####"], 1)  # escape ctrl+c strings
            continue
        ret = sess.wait2exec(["written: OK"], 300, "reset\n")
        if ret > 1:
            crt.Screen.Send("\3\r\n# script terminated for u.\r\n")
        if ret == 0:
            crt.Screen.Send("# fatal error occurred\r\n")
        break


genLip(crt)
exec_upgrade(crt)
