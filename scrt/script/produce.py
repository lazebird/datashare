import sys
import os

# define vars
sn = ""
mac = ""
pid = ""
ver = ""
max_mac = ""
max_mac_post = 0xFFFFFF


def debug(s):
    crt.Screen.Send("# " + s + "\n")


def args2str():
    return "SN=" + sn + "\nMAC=" + mac + "\nID=" + pid + "\nVER=" + ver + "\nMAX_MAC=" + max_mac


def property_file2line(filepath):
    s = ""
    try:
        f = open(filepath, "r")
        for line in f.readlines():
            line = line.strip().replace(" ", "")
            line = line if (line.find("#") < 0) else line[0 : line.find("#")]  # add comment support
            s = s + line + " "
        f.close()
    except:
        debug("File " + filepath + " not exists")
    return s


def cmdargs2line(obj):
    s = ""
    for index in range(obj.Count):
        s = s + obj[index] + " "
    return s


def opt_parse(s):
    opthash = {}
    s = s.replace('"', "")  # strip extra \"
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


def opts2args(opthash):
    global sn, mac, pid, ver, max_mac, max_mac_post
    if "SN" in opthash:
        sn = opthash["SN"]
    if "MAC" in opthash:
        mac = opthash["MAC"]
    if "ID" in opthash:
        pid = opthash["ID"]
    if "VER" in opthash:
        ver = opthash["VER"]
    if "MAX_MAC" in opthash:
        max_mac = opthash["MAX_MAC"]
    max_mac_post = int(max_mac[6:], 16) if max_mac != "" else 0xFFFFFF


def sint6_inc(s):
    i = int(s)
    # debug("sint6_inc: i=" + str(i) + ", i+1=" + str(i + 1) + ", base=" + str(base))
    if i == 999999:
        sys.exit(0)  # overflow
    return "{0:06d}".format(i + 1)


def shex6_inc(s):
    global max_mac_post
    i = int(s, 16)
    # debug("shex6_inc: i=" + str(i) + ", i+1=" + str(i + 1) + ", base=" + str(base))
    if i == max_mac_post:
        sys.exit(0)  # overflow
    return "{0:06X}".format(i + 1)


def do_info_inc():
    global sn, mac
    sn_pre = sn[0:6]
    sn_post = sn[6:]
    mac_pre = mac[0:6]
    mac_post = mac[6:]
    sn_post = sint6_inc(sn_post)
    mac_post = shex6_inc(mac_post)
    sn = sn_pre + sn_post
    mac = mac_pre + mac_post


def wait2uboot():
    ret = crt.Screen.WaitForStrings(
        ["stop with 'space'", "stop autoboot", "^C", "<INTERRUPT>"],
        0xFFFFFFF,
    )
    return ret == 1 or ret == 2


def do_product_set():
    crt.Screen.Send("product_set    " + pid + "    " + sn + "    " + mac + "    " + ver + "   \n")


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
        while True:
            do_product_set()
            ret = check_result()
            if ret < 0:
                return
            if ret == 0:
                continue
            do_info_inc()
            break
        # crt.Sleep(1000)


# init in code
# sn = "202106290001"
# mac = "FCCD2FD00001"
# pid = "LKST-6190-8GT2GS"
# ver = "V1.00"

# init by args
opts2args(opt_parse(cmdargs2line(crt.Arguments)))

# init by file? max_mac?
filepath = crt.Dialog.FileOpenDialog(title="Please select a file", filter="Config Files (*.txt;*.conf)|*.txt;*.conf|All Files(*.*)|*.*")
filepath != "" and opts2args(opt_parse(property_file2line(filepath)))

# init by prompt input
# sn = crt.Dialog.Prompt("Initial SN", "SN", sn)
# mac = crt.Dialog.Prompt("Initial MAC", "MAC", mac)
# pid = crt.Dialog.Prompt("Initial Product ID", "Product ID", pid)
# ver = crt.Dialog.Prompt("Initial Hardware Version", "Hardware Version", ver)

if sn != "" and mac != "":
    crt.Dialog.MessageBox(args2str(), "Initial Args", 64)
    main_loop()
crt.Dialog.MessageBox(args2str(), "Script Exit", 64)
