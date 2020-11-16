import sys
import os

(strScriptPath, strScriptName) = os.path.split(__file__)
# Inject the path to the script into sys.path for use when looking for modules
# to import.
if strScriptPath in sys.path:
    # If the path exists, don't inject.  Unless SecureCRT is closed, we don't
    # need to inject the path of the running script because sys.path is static.
    crt.Dialog.MessageBox("Already There!\n" + "sys.path: \n" + "\n".join(sys.path))
else:
    # Inject the path of the running script if it is not in sys.path
    sys.path.insert(0, strScriptPath)
    crt.Dialog.MessageBox("New Path Added!\n" + "sys.path: \n" + "\n".join(sys.path))
