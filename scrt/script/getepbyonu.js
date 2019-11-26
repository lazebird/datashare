var onumac;
onumac = crt.Dialog.Prompt("Please enter your ONU MAC like 74b9.ebc0.add5:")
if (onumac == "") {
	onumac="74b9.ebc0.add5";
}
var lines, arrays;
crt.Screen.Send("show onu | inc " + onumac + "\n          ");	
var onuinfo = crt.Screen.ReadString("OLT#");
lines = onuinfo.split("\n");
arrays = lines[1].split(/\s+/);
var ifname = arrays[0];
var llid = arrays[1];
crt.Screen.Send("#========== onu " + onumac + " interface " + ifname + ", llid " + llid + "\n");	
crt.Screen.WaitForString("OLT#");
var filter;
if (ifname.length == 7) {
	filter = ifname + "    " + llid + " ";
} else {
	filter = ifname + "   " + llid + " ";
}
crt.Screen.Send("show epon mac-address-table all | inc " + filter + "\n          ");	
var ponmacinfo = crt.Screen.ReadString("OLT#");
lines = ponmacinfo.split("\n");
for (var i = 1; i < lines.length; i++) {
	arrays = lines[i].split(/\s+/);
	var epmac = arrays[4];
	if (epmac) {
		if (epmac == "--") {
			//crt.Screen.Send("#========== line: " + lines[i] + "\n");	
			epmac = arrays[5];
		}
		crt.Screen.Send("#========== endpoint mac [" + i + "]: " + epmac + "\n");	
		crt.Screen.Send("show mac-address-table | inc " + epmac + "\n");	
	}
}
//crt.Dialog.MessageBox(ponmacinfo);
