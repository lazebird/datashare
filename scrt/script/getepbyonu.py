import re

onumac = crt.Dialog.Prompt("Please enter your ONU MAC like 74b9.ebc0.add5:") or "74b9.ebc0.add5"

lines, arrays
crt.Screen.Send("show onu | inc " + onumac + "\n          ")
onuinfo = crt.Screen.ReadString("OLT#")
lines = onuinfo.split("\n")
arrays = re.split("\s+", lines[1])
ifname = arrays[0]
llid = arrays[1]
crt.Screen.Send("#========== onu " + onumac + " interface " + ifname + ", llid " + str(llid) + "\n")
crt.Screen.WaitForString("OLT#")
filter
if ifname.length == 7:
    filter = ifname + "    " + str(llid) + " "
else:
    filter = ifname + "   " + str(llid) + " "

crt.Screen.Send("show epon mac-address-table all | inc " + filter + "\n          ")
ponmacinfo = crt.Screen.ReadString("OLT#")
lines = ponmacinfo.split("\n")
for i in range(1, lines.length):
    arrays = re.split("\s+", lines[i])
    epmac = arrays[4]
    if epmac:
        if epmac == "--":
            # crt.Screen.Send("#========== line: " + lines[i] + "\n")
            epmac = arrays[5]

        crt.Screen.Send("#========== endpoint mac [" + i + "]: " + epmac + "\n")
        crt.Screen.Send("show mac-address-table | inc " + epmac + "\n")


# crt.Dialog.MessageBox(ponmacinfo)
