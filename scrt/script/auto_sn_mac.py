import sys
import os

# define vars
sn = ""
mac = ""
pid = ""
ver = ""
test_flag = False


def debug(s):
    if test_flag and False:
        crt.Screen.Send("# " + s + "\n")


def parse_opt(obj):
    opthash = {}
    s = ""
    for index in range(obj.Count):
        s = s + obj[index] + " "
    s = s.replace("#", " ").replace(",", " ").replace("  ", " ").strip()
    pairs = s.split(" ")
    for tv in pairs:
        args = tv.split("=")
        if len(args) < 2:
            debug("invalid args: " + tv)
            continue
        opthash[args[0]] = args[1]
    return opthash


def chars_inc(s, base):
    i = int(s, base) + 1
    ret = str(i) if base == 10 else "{0:X}".format(i)
    debug("chars inc: i=" + str(i) + ", base=" + str(base) + ", ret=" + ret)
    return ret.zfill(len(s))  # may be overflow


def wait2uboot():
    timeout = 0xFFFFFFF
    if test_flag:
        timeout = 2
    ret = crt.Screen.WaitForStrings(
        ["stop with 'space'", "stop autoboot", "^C", "<INTERRUPT>"],
        timeout,
    )
    return ret == 1 or ret == 2 or (test_flag and ret == 0)


def do_info_inc():
    global sn, mac
    debug("before inc: sn=" + sn + ", mac=" + mac)
    sn_pre = sn[0:8]
    sn_post = sn[8:]
    mac_pre = mac[0:8]
    mac_post = mac[8:]
    sn_post = chars_inc(sn_post, 10)
    mac_post = chars_inc(mac_post, 16)
    sn = sn_pre + sn_post
    mac = mac_pre + mac_post
    debug("after  inc: sn=" + sn + ", mac=" + mac)


def do_product_set():
    if test_flag:
        crt.Screen.Send("# ")
    crt.Screen.Send("product_set    " + pid + "    " + sn + "    " + mac + "    " + ver + "   \n")
    ret = 0
    # ret = crt.Screen.WaitForStrings(["success", "fail"], 1) # read result
    ok = crt.Dialog.Prompt("Success?", "Confirmation", "ok")
    if ok == "exit" or ok == "quit":
        sys.exit(0)
    if ok != "":
        ret = 1
    return ret == 1


# init in code
sn = "202106290001"
mac = "FCCD2FD0000A"
pid = "LKST-6190-8GT2GS"
ver = "V1.00"

# init by command args
opthash = parse_opt(crt.Arguments)
if "sn" in opthash:
    sn = opthash["sn"]
if "mac" in opthash:
    mac = opthash["mac"]
if "id" in opthash:
    pid = opthash["id"]
if "ver" in opthash:
    ver = opthash["ver"]

# init by prompt input
sn = crt.Dialog.Prompt("Initial SN", "SN", sn)
mac = crt.Dialog.Prompt("Initial MAC", "MAC", mac)
pid = crt.Dialog.Prompt("Initial Product ID", "Product ID", pid)
ver = crt.Dialog.Prompt("Initial Hardware Version", "Hardware Version", ver)

if sn != "" and mac != "":
    while True:
        if not wait2uboot():
            break
        crt.Screen.Send("#    \n")
        crt.Sleep(1000)
        if do_product_set():
            do_info_inc()

crt.Dialog.MessageBox("#script exit")
