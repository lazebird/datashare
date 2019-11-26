# $language = "VBScript"
# $interface = "1.0"



Sub Main

    Dim pc_ip, devip_pre, devip_post, devip, dataname, rootfsname
    pc_ip = "192.168.100.106"
    devip_pre = "192.168.100."   
    devip_post = (Timer AND 63) + 107   ' concurrency 64, start 107
    devip = devip_pre & devip_post 
    dataname = "data.ubi"
    rootfsname = "rootfs.ubi"

cmd "update_data "&pc_ip&" "&devip&" "&dataname   'UBI文件根据实际需要来进行选择

if crt.screen.waitforstring("[y/N]")<>True  then '等待起
end if

crt.sleep 1000

crt.screen.send "y"

crt.screen.send vbCR

if crt.screen.waitforstring("written: OK")<>True  then '等待起
end if

crt.sleep 1000


cmd "update_rootfs "&pc_ip&" "&devip&" "&rootfsname

if crt.screen.waitforstring("bootloader#")<>True  then '等待起
end if

crt.sleep 1000

cmd "reset"


end Sub

'=============================================================
' 必要的延时
'
sub cmd (Var)
    Dim Str, cmd_length, ptr
    cmd_length = Len(Var)
    ptr = 1
    While cmd_length >= ptr
        Str = Mid(Var, ptr, 8)
        crt.screen.send Str 
        crt.sleep 200
        ptr = ptr + 8
    Wend
    crt.screen.send vbCR
    crt.sleep 500
End sub