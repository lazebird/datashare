import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
crt.Dialog.MessageBox("sys.path: \n" + "\n".join(sys.path))
