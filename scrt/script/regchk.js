var loopcmdnum = parseInt(30);
var timeout = parseInt(3);
var prompt1="login:";
var prompt2="xxxxxx"; // unused
var intr1="^C";
var intr2="<INTERRUPT>";

var cmdarray=new Array(
	"diagnostic register write 0 0x2040004 ", //0x81700000", 
	"diagnostic register read 0 0x2040150");

function execcmd(cmdstr)
{
	crt.Screen.Send(cmdstr+"\n");
}

function wait4pause(time)
{
	var ret = crt.Screen.WaitForStrings("^C", "<INTERRUPT>", time);
	if (ret > 0) {
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

function addZero(str,length){               
    return new Array(length - str.length + 1).join("0") + str;              
}

function cmdloop(num)
{
	var i, data, lastdata;
	for (i = 1; i < 20; i++) {
		lastdata = 0;
		execcmd(cmdarray[0] + "0x8" + addZero(i + "", 2) + "00000");
		crt.Screen.ReadString("SWITCH#", 1);
		var j;
		for (j = 0; j < 2; j++) {
			execcmd(cmdarray[1]);
			var re = /rv 0 data (\w+)/g;
			var re1 = /\r*\n/g;
			data = crt.Screen.ReadString("SWITCH#", 1);
			data = data.replace(re1, ";");
			//crt.Screen.Send("#data "+data+"\n");
			data = re.exec(data)[1];
			crt.Screen.ReadString("SWITCH#", 1);
			if (lastdata && lastdata != data) {
				crt.Screen.Send("####################### loop "+i+" data "+data+" lastdata "+lastdata+"#######################\n");
				crt.Screen.ReadString("SWITCH#", 1);
				break;
				//return 0;
			}
			lastdata = data;
			if (wait4pause(2)) {
				return 0;
			}
		}
	}
	return 0;
}

//while (cmdloop(loopcmdnum) && cmdreboot() && cmdwait2login());
while (cmdloop(loopcmdnum));
crt.Screen.Send("#game over!\n");
