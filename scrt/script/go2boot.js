var ret = null;
var prompt1="autoboot";
crt.Screen.Send("\x1a\x1a\x1a");

crt.Screen.Send("\r\n");
ret = crt.Screen.WaitForStrings("login", 1);
if (ret == 1) { // login first
	crt.Screen.Send("admin\r\n");
	crt.Screen.WaitForStrings("Password", 3);
	crt.Screen.Send("admin\r\n");
	crt.Screen.WaitForStrings(">", 3);
	crt.Screen.Send("enable\r\n");
}

crt.Screen.Send("entershell\r\n");
crt.Screen.Send("reboot\r\n");
while (ret != 2 && ret != 3) {
	ret = crt.Screen.WaitForStrings(prompt1, "^C", "<INTERRUPT>");
	if (ret == 1) crt.Screen.Send(" \r\n");
}

