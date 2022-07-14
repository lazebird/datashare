timeout = 5
portnum = 10
llidperport = 30
macfmt = "0000.0000.0000"
ret = 4
for i in (1, portnum):
    crt.Screen.Send("interface epon0/" + i + "\n")
    for j in (0, llidperport):
        macpost = (i + j * llidperport).toString()
        mac = macfmt.substr(0, macfmt.length - macpost.length) + macpost
        crt.Screen.Send(" onu bind mac-address " + mac + " llid " + j + "\n")
        ret = crt.Screen.WaitForStrings(["^C", "<INTERRUPT>", "^Z", "#"], int(timeout))
        if ret <= 3:
            break
    crt.Screen.Send("exit\n")
    if ret <= 3:
        break


crt.Screen.Send("#ret " + ret + "\n")
