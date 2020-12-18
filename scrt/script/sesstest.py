import sys
# import os

# (strScriptPath, strScriptName) = os.path.split(__file__)
# if strScriptPath not in sys.path:
# 	sys.path.insert(0, strScriptPath)
# sys.dont_write_bytecode = True

# import session
# import log

# sess = session.sess(crt.GetActiveTab())
# sess.cmdexec("interface eth0/1", "abc")
# sess.cmdexec("show version")

crt.Screen.Synchronous = True
crt.Screen.IgnoreEscape = True
crt.Screen.Send("\n")
crt.Screen.WaitForStrings(["should never be matched"], 1) # clear screen buffer
lastcol = crt.Screen.CurrentColumn
lastrow = crt.Screen.CurrentRow
crt.Screen.Send("show version" + "\n")
output = crt.Screen.ReadString(["#"], 3)
curcol = crt.Screen.CurrentColumn
currow = crt.Screen.CurrentRow
msg = crt.Screen.Get2(lastrow, lastcol, curcol, currow)
ret = crt.Screen.MatchIndex
crt.Dialog.MessageBox(crt.GetActiveTab().Caption + ": ret " + str(ret) + ", output " + output)
crt.Dialog.MessageBox("("+str(lastrow)+","+str(lastcol)+") - ("+str(currow)+","+str(curcol)+")")
crt.Dialog.MessageBox(crt.GetActiveTab().Caption + ": msg: " + msg)
