var selectedport = "";
function setportevt() {
  for (var i = 1; i < 9; i++) {
    var port = document.getElementById("port" + i);
  }
}
function genMsg(e) {
  var msg = e.id + ":" + "\n";
  msg += "  speed: 1000M, duplex: Full" + "\n";
  msg += "  ingress: 10kBps, egress: 3kBps" + "\n";
  msg += " \nmore detail >>>";
  // console.log(msg);
  return msg;
}
function msg2text(t, msg) {
  var lines = msg.split("\n");
  for (const v of lines) {
    var tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
    tspan.setAttribute("x", t.getAttribute("x"));
    tspan.setAttribute("dy", "1.2em");
    tspan.textContent = v;
    t.appendChild(tspan);
  }
}
function onSelect(e) {
  var desc = document.getElementById("desc");
  desc.textContent = "";
  if (e.id === selectedport) {
    selectedport = "";
    return;
  }
  selectedport = e.id;
  msg2text(desc, genMsg(e));
}
function click2go() {
  if (selectedport === "") {
    return;
  }
  var desc = document.getElementById("desc");
  desc.textContent = "here we go to detail page of " + selectedport + " ...";
}
