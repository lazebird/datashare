// 测试vrrp重启后实例未就绪问题
var loopcmdnum = parseInt(10);
var timeout = parseInt(10);
var prompt1 = "login:";
var prompt2 = "xxxxxx"; // unused
var intr1 = "^C";
var intr2 = "<INTERRUPT>";
var bug_found = false;

function iobuf_empty() {
  crt.Screen.WaitForStrings("[should never be read]", intr1, intr2, 1);
}

function init_debug() {
  crt.Screen.Send("./guard.sh\n");
}
// avoid flash full
function do_clean() {
  crt.Screen.Send("entershell\ncd /var/log\n");
  crt.Screen.Send("rm -rf message syslog kern.log user.log wtmp\n");
  return 1;
}

function bug_check() {
  iobuf_empty();
  crt.Screen.Send("rm -rf output/*/ && rm -rf output/*.done\n");
  var ret = crt.Screen.WaitForStrings("FAILED", 1);
  bug_found = ret == 1;
  crt.Screen.Send("tree output/\n");
  return ret == 1;
}

function wait4pause(time) {
  var ret = crt.Screen.WaitForStrings("^C", "<INTERRUPT>", time);
  if (ret > 0) {
    //crt.Sleep(10000);
    crt.Screen.Send("###user terminated(" + ret + ")!\n");
    return 1;
  }
  return 0;
}

function cmdreboot() {
  crt.Screen.Send("end\nentershell\n");
  // crt.Screen.Send("cat /var/log/crash.log\n");
  //   crt.Screen.Send("ls -l /var/core/\n");
  crt.Screen.Send("reboot\n");
  return 1;
}

function cmdwait2login() {
  var ret = null;
  while (ret == "" || ret == undefined || ret == null) {
    ret = crt.Screen.WaitForStrings(prompt1, prompt2, intr1, intr2);
  }
  if (ret == 1 || ret == 2) {
    crt.Screen.Send("admin\n");
    crt.Sleep(500);
    crt.Screen.Send("admin\n");
    crt.Sleep(1000);
    crt.Screen.Send("enable\n");
    // crt.Sleep(5000); // wait for a moment, make sure system started.
    return !wait4pause(30); // wait for a moment, make sure system started.
  } else {
    return 0;
  }
}

init_debug();
while (!bug_check() && !wait4pause(3));
//while (!wait4pause(300) && cmdreboot() && cmdwait2login());
crt.Screen.Send(bug_found ? "#Bug Found!\n" : "#Game Over!\n");
if (bug_found) crt.Dialog.MessageBox("Bug Found!");
