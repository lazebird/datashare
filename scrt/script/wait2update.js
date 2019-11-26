# $language = "javascript"
# $interface = "1.0"

var ret = null;
var prompt1 = "bootloader#";
var prompt2 = ">>";
var intr1 = "^C";
var intr2 = "<INTERRUPT>";
var progress1 = "Bytes";
var progress2 = "#";
var done1 = "[Done]";
var done2 = "OK";
var srvip = "192.168.100.106";//"10.1.1.2";
var myDate = new Date();
var cursec = myDate.getSeconds(); // [0,59]
var ip_pending = cursec + 190;
var localip = srvip.substring(0, srvip.lastIndexOf('.') + 1) + ip_pending; // [190,250]
while (ret == "" || ret == undefined || ret == null) {
	crt.Screen.Send(" \r\n");
	ret = crt.Screen.WaitForStrings(prompt1, prompt2, intr1, intr2, 1);
}

ret = ((ret == 1 || ret == 2) ? null : -1);
//crt.Screen.Send("#ret "+ret+"\r\n");
while (ret == "" || ret == undefined || ret == null) {
	crt.Screen.Send("update_rootfs " + srvip + " " + localip + " rootfs.ubi\r\n");
	ret = crt.Screen.WaitForStrings(progress1, progress2, intr1, intr2, 3);
}

ret = ((ret == 1 || ret == 2) ? null : -1);
while (ret == "" || ret == undefined || ret == null) {
	ret = crt.Screen.WaitForStrings(prompt1, prompt2, done1, done2, intr1, intr2, 300);
}

if (ret == 3 || ret == 4) {
	crt.Screen.Send("reset\r\n");
} else {
	crt.Screen.Send("#err " + ret + "\r\n");
}