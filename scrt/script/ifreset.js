var timeout = 30;
var ifarray = new Array("eth0/7", "eth0/8");

function shutdown(ifname) {
  crt.Screen.Send("interface " + ifname + "\n");
  crt.Screen.Send("shutdown\n");
  crt.Screen.Send("exit\n");
}

function noshutdown(ifname) {
  crt.Screen.Send("interface " + ifname + "\n");
  crt.Screen.Send("no shutdown\n");
  crt.Screen.Send("exit\n");
}

function wait4pause(time) {
  return crt.Screen.WaitForStrings("^C", "<INTERRUPT>", "^Z", parseInt(time)); //crt.Sleep(10000);
}

var loop = 1;
while (loop == 1) {
  for (i in ifarray) {
    shutdown(ifarray[i]);
    var tout = Math.floor(Math.random() * 120) + 1; // 0 means infinite
    if (wait4pause(tout)) {
      loop = 0;
      break;
    }
    noshutdown(ifarray[i]);
    var tout = Math.floor(Math.random() * 120) + 1; // 0 means infinite
    crt.Screen.send("#tout " + tout + "\n");
    if (wait4pause(tout)) {
      loop = 0;
      break;
    }
  }
}
crt.Screen.Send("#script exit\n");
