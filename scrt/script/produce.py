import sys
import os

# define vars
sn = ""
mac = ""
pid = ""
ver = ""


def debug(s):
    crt.Screen.Send("# " + s + "\n")


def parse_opt(obj):
    opthash = {}
    s = ""
    for index in range(obj.Count):
        s = s + obj[index] + " "
    s = s.replace("#", " ")  # support '#' as ' '
    s = s.replace(",", " ")  # support ',' as ' '
    s = s.replace("  ", " ")  # support '  ' as ' '
    s = s.strip()
    pairs = s.split(" ")
    for tv in pairs:
        args = tv.split("=")
        if len(args) < 2:
            # debug("invalid args: " + tv)
            continue
        opthash[args[0]] = args[1]
    return opthash


def char6_inc(s, base):
    i = int(s, base)
    # debug("char6 inc: i=" + str(i) + ", i+1=" + str(i + 1) + ", base=" + str(base))
    i = i + 1
    if base == 10:
        return "{0:06d}".format(i)
    return "{0:06X}".format(i)


def wait2uboot():
    ret = crt.Screen.WaitForStrings(
        ["stop with 'space'", "stop autoboot", "^C", "<INTERRUPT>"],
        0xFFFFFFF,
    )
    return ret == 1 or ret == 2


def do_info_inc():
    global sn, mac
    # debug("before inc: sn=" + sn + ", mac=" + mac)
    sn_pre = sn[0:6]
    sn_post = sn[6:]
    mac_pre = mac[0:6]
    mac_post = mac[6:]
    sn_post = char6_inc(sn_post, 10)
    mac_post = char6_inc(mac_post, 16)
    sn = sn_pre + sn_post
    mac = mac_pre + mac_post
    # debug("after  inc: sn=" + sn + ", mac=" + mac)


def do_product_set():
    crt.Screen.Send(
        "product_set    " + pid + "    " + sn + "    " + mac + "    " + ver + "   \n"
    )


def check_result():
    # ret = crt.Screen.WaitForStrings(["Success", "Fail"], 1) # read result
    ok = crt.Dialog.Prompt("Success?", "Confirmation", "ok")
    if ok == "":
        return 0
    if ok == "ok":
        return 1
    return -1


def main_loop():
    while True:
        if not wait2uboot():
            break
        crt.Screen.Send("#    \n")
        crt.Sleep(1000)
        do_product_set()
        ret = check_result()
        if ret < 0:
            break
        if ret == 1:
            do_info_inc()
        # crt.Sleep(1000)


# init in code
sn = "202106290001"
mac = "FCCD2FD00001"
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
    main_loop()
crt.Dialog.MessageBox("SN=" + sn + "\nMAC=" + mac, "#script exit")
