var myDate = new Date();
var cursec = myDate.getSeconds(); // [0,59]
var randseed = cursec%10;
var loopcmdnum = parseInt(10 + randseed);
var timeout = parseInt(180 + randseed);
var prompt1="login:";
var prompt2="RETURN"; // unused
var intr1="^C";
var intr2="<INTERRUPT>";

var cmdarray=new Array(
	"no igmp snooping\r\n",
	"end\r\n show igmp snooping all\r\n show diagnostic igmp\r\n conf t\r\n igmp snooping\r\n");

function execcmd(cmdstr)
{
	crt.Screen.Send(cmdstr+"\n");
}

function wait4pause(time)
{
	var ret = crt.Screen.WaitForStrings("^C", "<INTERRUPT>", time);
	if (ret > 0) { //crt.Sleep(10000);
		crt.Screen.Send("###user terminated("+ret+")!\n");
		return 1;
	}
	return 0;
}

function cmdreboot()
{
	crt.Screen.Send("end\nentershell\n");
	crt.Screen.Send("cat /var/log/crash.log\n");
	crt.Screen.Send("reboot\n");
	return 1;
}

function cmdpreconfig()
{
	crt.Screen.Send("enable\nethernet cfm debug erps\nconfig t\n");
	return 1;
}

function cmdwait2login()
{
	var ret = null;
	while (ret == "" || ret == undefined || ret == null) {
		ret = crt.Screen.WaitForStrings(prompt1, prompt2, intr1, intr2);
	}
	if (ret == 1 || ret == 2) {
		crt.Screen.Send("admin\n");
		crt.Sleep(500);
		crt.Screen.Send("admin\n");
		crt.Sleep(1000);
		// crt.Screen.Send("enable\nethernet cfm debug erps\nconfig t\n"); // cmdpreconfig()
		// crt.Sleep(5000); // wait for a moment, make sure system started.
		return !wait4pause(5) && cmdpreconfig(); // wait for a moment, make sure system started.
	} else {
		return 0;
	}
}

function cmdloop(num)
{
	var ret = 1;
	execcmd(cmdarray[0]);
	ret = !wait4pause(1);
	execcmd(cmdarray[1]);
	return ret;
}

crt.Screen.send("#loopcmdnum " + loopcmdnum + " timeout " + timeout + "\n");
//while (cmdloop(loopcmdnum) && cmdreboot() && cmdwait2login());
while (cmdloop(loopcmdnum) && !wait4pause(timeout));
crt.Screen.Send("#game over!\n");

