import sys
import time

srvip = "192.168.100.106"#"10.1.1.2"
if len(sys.argv) > 1:
    srvip = sys.argv[1]

ret = 0
prompt1 = "bootloader#"
prompt2 = ">>"
intr1 = "^C"
intr2 = "<INTERRUPT>"
progress1 = "Bytes"
progress2 = "#"
done1 = "[Done]"
done2 = "OK"
mytime = int(time.time())
cursec = mytime%60 # [0,59]
ip_pending = str(cursec + 190)
localip = srvip[0:srvip.rindex('.') + 1] + ip_pending # [190,250]
while ret == "" or ret == 0: 
	crt.Screen.Send(" \r\n")
	ret = crt.Screen.WaitForStrings([prompt1, prompt2, intr1, intr2], 1)


ret = 0 if ret == 1 or ret == 2 else -1
#crt.Screen.Send("#ret "+ret+"\r\n")
while ret == "" or ret == 0: 
	crt.Screen.Send("update_rootfs0 " + srvip + " " + localip + " rootfs.ubi\r\n")
	ret = crt.Screen.WaitForStrings([progress1, progress2, intr1, intr2], 3)


ret = 0 if ret == 1 or ret == 2 else -1
while ret == "" or ret == 0: 
	ret = crt.Screen.WaitForStrings([prompt1, prompt2, done1, done2, intr1, intr2], 300)


if ret == 3 or ret == 4: 
	crt.Screen.Send("reset\r\n")
else: 
	crt.Screen.Send("#err " + str(ret) + "\r\n")
