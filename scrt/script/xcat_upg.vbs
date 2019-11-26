# $language = "VBScript"
# $interface = "1.0"

Sub Main
    Dim pc_ip, devip_prefix, devip_suffix, devip, dataname, rootfsname
    pc_ip = "192.168.100.106"
    devip_prefix = "192.168.100."   
    devip_suffix = (Timer AND 63) + 107   ' concurrency 64, start 107
    devip = devip_prefix & devip_suffix 
    dataname = "data.ubi"
    rootfsname = "rootfs.ubi"

    crt.screen.send "update_data "&pc_ip&" "&devip&" "&dataname&vbCRLF
    if crt.screen.waitforstring("[y/N]")  then
        crt.screen.send "y"&vbCR
    end if
    if crt.screen.waitforstring("bootloader#")  then
        crt.screen.send "#"&vbCRLF      ' clear io buf
        if crt.screen.waitforstring("bootloader#")  then
        end if
        crt.screen.send "update_rootfs "&pc_ip&" "&devip&" "&rootfsname&vbCRLF
        if crt.screen.waitforstring("bootloader#")  then
            crt.screen.send "#"&vbCRLF      ' clear io buf
            if crt.screen.waitforstring("bootloader#")  then
            end if
            crt.screen.send "reset"&vbCRLF
        end if
    end if
end Sub
