# $language = "JScript"
# $interface = "1.0"

opts = crt.Arguments.Count == 1 ? json.loads(crt.Arguments[0]) : undefined

crt.Screen.Send("\r\n#opts=" + str(opts) + "\r\n")
