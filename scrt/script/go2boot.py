import sys, os, json

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

from utils import session

sess = session.sess(crt.GetActiveTab())
opts = json.loads(crt.Arguments[0]) if crt.Arguments.Count == 1 else {}

loopcnt = opts.get("count", 1)
key = opts.get("key")

if not sess.is_uboot():
    sess.try_login()
    sess.cmdreboot(key=key)
while loopcnt > 0:
    loopcnt = loopcnt - 1
    if not sess.wait2uboot():
        break
