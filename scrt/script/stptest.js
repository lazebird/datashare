var loopcmdnum = 5 + Math.floor(Math.random() * 10);
var timeout = 5 + Math.floor(Math.random() * 10);
var prompt1 = "login:";
var prompt2 = "RETURN"; // unused
var intr1 = "^C";
var intr2 = "<INTERRUPT>";

var cmdarray = new Array(
  "interface eth0/7\r\nshutdown\r\nexit",
  "interface eth0/7\r\nno shutdown\r\nexit",
  "interface eth0/8\r\nshutdown\r\nexit",
  "interface eth0/8\r\nno shutdown\r\nexit"
);

function execcmd(cmdstr) {
  crt.Screen.Send(cmdstr + "\n");
}

function wait4pause(time) {
  var ret = crt.Screen.WaitForStrings("^C", "<INTERRUPT>", time);
  if (ret > 0) {
    crt.Screen.Send("###user terminated(" + ret + ")!\n");
    return 1;
  }
  return 0;
}

function cmdreboot() {
  crt.Screen.Send("end\nentershell\n");
  crt.Screen.Send("reboot\n");
  return 1;
}

function cmdpreconfig() {
  crt.Screen.Send("enable\nconfig t\n");
  return 1;
}

function cmdwait2login() {
  var ret = crt.Screen.WaitForStrings(prompt1, prompt2, intr1, intr2);
  if (ret == 1 || ret == 2) {
    crt.Screen.Send("admin\n");
    crt.Sleep(500);
    crt.Screen.Send("admin\n");
    crt.Sleep(1000);
    return !wait4pause(5) && cmdpreconfig(); // wait for a moment, make sure system started.
  } else {
    return 0;
  }
}

function cmdloop(num) {
  while (num-- && !wait4pause(timeout)) {
    execcmd(cmdarray[Math.floor(Math.random() * cmdarray.length)]);
  }
  return num == -1;
}

crt.Screen.send("#loopcmdnum " + loopcmdnum + " timeout " + timeout + "\n");
while (cmdloop(loopcmdnum) && cmdreboot() && cmdwait2login());
crt.Screen.Send("#game over!\n");
