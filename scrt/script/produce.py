import sys
import os

# define vars
sn = ""
mac = ""


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
            # crt.Screen.Send("# invalid args: " + tv)
            continue
        opthash[args[0]] = args[1]
    return opthash


def char4_inc(s, base):
    i = int(s, base)
    # debug("char4 inc: i=" + str(i) + ", i+1=" + str(i + 1) + ", base=" + str(base))
    i = i + 1
    if base == 10:
        return "{0:04d}".format(i)
    return "{0:04X}".format(i)


def wait2uboot():
    ret = crt.Screen.WaitForStrings(
        ["stop with 'space'", "stop autoboot:", "^C", "<INTERRUPT>"],
        0xFFFFFFF,
    )
    return ret == 1 or ret == 2


def do_info_inc():
    global sn, mac
    # debug("before inc: sn=" + sn + ", mac=" + mac)
    sn_pre = sn[0:8]
    sn_post = sn[8:]
    mac_pre = mac[0:8]
    mac_post = mac[8:]
    sn_post = char4_inc(sn_post, 10)
    mac_post = char4_inc(mac_post, 16)
    sn = sn_pre + sn_post
    mac = mac_pre + mac_post
    # debug("after  inc: sn=" + sn + ", mac=" + mac)


def do_product_set():
    crt.Screen.Send("product_set MAC3L-8GT4GS-1R1IO  " + sn + " " + mac + " V1.20 \n")
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
mac = "04111980020A"

# init by command args
opthash = parse_opt(crt.Arguments)
if "sn" in opthash:
    sn = opthash["sn"]
if "mac" in opthash:
    mac = opthash["mac"]

# init by prompt input
sn = crt.Dialog.Prompt("Initial SN", "SN", sn)
mac = crt.Dialog.Prompt("Initial MAC", "MAC", mac)

if sn != "" and mac != "":
    while True:
        wait2uboot()
        if do_product_set():
            do_info_inc()
        # crt.Sleep(1000)
