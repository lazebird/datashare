import sys, os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

from utils import opt, session

sess = session.sess(crt.GetActiveTab())
opts = opt.opt(crt.Arguments)

loopcnt = opts.getval("count") or 1
key = opts.getval("key")

if not sess.is_uboot():
    sess.try_login()
    sess.cmdreboot(key=key)
while loopcnt > 0:
    loopcnt = loopcnt - 1
    if not sess.wait2uboot():
        break
