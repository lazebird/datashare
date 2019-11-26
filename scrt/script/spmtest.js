var loopcmdnum = parseInt(30);
var timeout = parseInt(5);
var prompt1="login:";
var prompt2="xxxxxx"; // unused
var intr1="^C";
var intr2="<INTERRUPT>";

var cmdarray=new Array(
	"spanning-tree mode rstp", 
	"spanning-tree mode stp", 
	"spanning-tree mode provider-rstp edge", 
	"spanning-tree mode mstp", 
	"end\r\nshow vlan all\r\n \r\n \r\n \r\n \r\n \r\n \r\nconf t", 
	"vlan 2-10 type service point", 
	"vlan 2-10", 
	"spanning-tree enable", 
	"igmp snooping");

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
		crt.Screen.Send("enable\nconfig t\n");
		// crt.Sleep(5000); // wait for a moment, make sure system started.
		return !wait4pause(5); // wait for a moment, make sure system started.
	} else {
		return 0;
	}
}

function cmdloop(num)
{
	//crt.Screen.Send("logging level nsm 7\nlogging console 7\n");
	while (num-- && !wait4pause(timeout)) {
		execcmd(cmdarray[Math.floor(Math.random()*cmdarray.length)]);
	}
	return (num == -1);
}

//while (cmdloop(loopcmdnum) && cmdreboot() && cmdwait2login());
while (cmdloop(loopcmdnum));
crt.Screen.Send("#game over!\n");

