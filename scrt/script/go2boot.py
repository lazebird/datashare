import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
	sys.path.insert(0, strScriptPath)

import devutils

loopcnt = 1
if crt.Arguments.Count > 0:
	loopcnt = int(crt.Arguments[0])
prompt1 = "autoboot"
devutils.try_login(crt)
devutils.cmdreboot(crt)
while loopcnt > 0:
	loopcnt = loopcnt - 1
	if not devutils.wait2uboot(crt):
		break
