var timeout = 5;
var portnum = 10;
var llidperport = 30;
var macfmt = "0000.0000.0000";
var ret = 4;
for (var i = 1; i <= portnum && ret > 3; i++) {
	crt.Screen.Send("interface epon0/"+i+"\n");
	for (var j = 0; j < llidperport && ret > 3; j++) {
		var macpost = (i + j * llidperport).toString();
		var mac = macfmt.substr(0, macfmt.length - macpost.length) + macpost;
		crt.Screen.Send(" onu bind mac-address " + mac + " llid "+j+"\n");
		ret = crt.Screen.WaitForStrings("^C", "<INTERRUPT>", "^Z", "#", parseInt(timeout)); //crt.Sleep(10000);
	}
	crt.Screen.Send("exit\n");
}
crt.Screen.Send("#ret "+ret+"\n");
