import sys, os, json

(strScriptPath, strScriptName) = os.path.split(__file__)
if strScriptPath not in sys.path:
    sys.path.insert(0, strScriptPath)
sys.dont_write_bytecode = True

from utils import log, file

opts = json.loads(crt.Arguments[0]) if crt.Arguments.Count == 1 else None

crt.Screen.Send("\r\n#opts=" + str(opts) + "\r\n")
