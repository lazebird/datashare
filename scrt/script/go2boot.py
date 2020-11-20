import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

import session

sess = session.sess(crt)

loopcnt = 1
if crt.Arguments.Count > 0:
	loopcnt = int(crt.Arguments[0])
if not sess.is_uboot():
	sess.try_login()
	sess.cmdreboot()
while loopcnt > 0:
	loopcnt = loopcnt - 1
	if not sess.wait2uboot():
		break
