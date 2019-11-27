-- 定义协议，可以在wireshark中使用cmportal过滤
cmportal_proto = Proto("cmportalv2","cmportalv2","cmportalv2 Protocol")
-- dissector函数
function cmportal_proto.dissector(buffer,pinfo,tree)
   
    --pinfo的成员可以参考用户手册
    pinfo.cols.protocol = "cmportalv2"
   
    local subtree = tree:add(cmportal_proto,buffer(),"cmportalv2 Protocol")
          
    --不对应任何数据
    subtree:add(buffer(0,16),"Header: ")
   
    --版本号对应于第一个字节
    subtree:add(buffer(0,1),"  Version: " .. buffer(0,1):uint())
    ver = buffer(0,1):uint()
	
    --类型对应于第二个字节
    type = buffer(1,1):uint()
    type_str = "Unknown"
    if type == 1 then
        type_str = "REQ_CHALLENGE"
    elseif type == 2 then
        type_str = "ACK_CHALLENGE"
    elseif type == 3 then
        type_str = "REQ_AUTH"
    elseif type == 4 then
        type_str = "ACK_AUTH"
    elseif type == 5 then
        type_str = "REQ_LOGOUT"
    elseif type == 6 then
        type_str = "ACK_LOGOUT"
    elseif type == 7 then
        type_str = "AFF_ACK_AUTH"
    elseif type == 8 then
        type_str = "NTF_LOGOUT"
    elseif type == 9 then
        type_str = "REQ_INFO"
    elseif type == 0xa then
        type_str = "ACK_INFO"
    elseif type == 0x30 then
        type_str = "REQ_BINDING_INFO"
    elseif type == 0x31 then
        type_str = "ACK_BINDING_INFO"
    elseif type == 0x32 then
        type_str = "NTF_USER_LOGON"
    elseif type == 0x34 then
        type_str = "NTF_USER_LOGOFF"
    elseif type == 0x36 then
        type_str = "REQ_USER_OFFLINE"		
    end
    subtree:add(buffer(1,1), "  Type: " .. type_str)

		--PAP/CHAP
    mode = buffer(2,1):uint()
    mode_str = "Unknown"
    if mode == 0 then
        mode_str = "CHAP"
    elseif mode == 1 then
        mode_str = "PAP"
    end
     subtree:add(buffer(2,1), "  Mode: " .. mode_str)

		--RSV
    rsv = string.format("%d", buffer(3,1):uint())
    rsv_str = "Unknown"
    subtree:add(buffer(3,1), "  RSV: " .. rsv)

		--SerialNo
    num = string.format("%d", buffer(4,2):uint())
    subtree:add(buffer(4,2), "  SerialNo: "..num)

		--ReqID
    reqid = string.format("%d", buffer(6,2):uint())
    subtree:add(buffer(6,2), "  ReqID: "..reqid)
	size = buffer:len()
	do
		--UserIP
    userip = string.format("%d.", buffer(8,1):uint())
    userip = userip .. string.format("%d.", buffer(9,1):uint())
    userip = userip .. string.format("%d.", buffer(10,1):uint())
    userip = userip .. string.format("%d", buffer(11,1):uint())
    subtree:add(buffer(8,4), "  UserIP: "..userip)

		--UserPort
    userport = string.format("%d", buffer(12,2):uint())
    subtree:add(buffer(12,2), "  UserPort: "..userport)

		--ERRCODE
    errcode = string.format("%d", buffer(14,1):uint())
    subtree:add(buffer(14,1), "  ERRCODE: "..errcode)

		--ATTRNUM
    attrnum = string.format("%d", buffer(15,1):uint())
    subtree:add(buffer(15,1), "  ATTRNUM: "..attrnum)

	if ver == 2 then
		subtree:add(buffer(16, 16), "  Authenticator: "..buffer(16,16))
	end
	
    --数据    
	if ver == 1 then
		pos = 16
	elseif ver == 2 then
		pos = 32
	end    
	if buffer(15,1):uint() > 0 then
		subtree:add(buffer(pos,size - pos), "Attribute: ")	
	end
	end
	
    while pos < size do
    		atype = buffer(pos, 1):uint()
    		pos = pos + 1
    		alen = buffer(pos, 1):uint()
    		pos = pos + 1
    		aval = buffer(pos, alen - 2):string()
    		pos = pos + alen -2
    		if atype == 1 then
    			subtree:add(buffer(pos - alen, alen), "  UserName(T1,L"..alen.."): "..aval)
    		elseif atype == 2 then
    			subtree:add(buffer(pos - alen, alen), "  PassWord(T2,L"..alen.."): "..aval)
    		elseif atype == 3 then
    			subtree:add(buffer(pos - alen, alen), "  Challenge(T3,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))
    		elseif atype == 4 then
    			subtree:add(buffer(pos - alen, alen), "  ChapPassWord(T4,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))
			elseif atype == 5 then
				subtree:add(buffer(pos - alen, alen), "  Replymsg(T5,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))				
    		elseif atype == 8 then
    			subtree:add(buffer(pos - alen, alen), "  NasPortId(T8,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))				
    		elseif atype == 0xa then
    			subtree:add(buffer(pos - alen, alen), "  BasIp(T10,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))
    		elseif atype == 0xb then
    			subtree:add(buffer(pos - alen, alen), "  SessionId(T11,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))				
    		elseif atype == 0x30 then
    			subtree:add(buffer(pos - alen, alen), "  NasId(T48,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))				
    		elseif atype == 0x31 then
    			subtree:add(buffer(pos - alen, alen), "  SessionStart(T49,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))					
    		elseif atype == 0x32 then
    			subtree:add(buffer(pos - alen, alen), "  SessionStop(T50,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))	
    		elseif atype == 0x33 then
    			subtree:add(buffer(pos - alen, alen), "  SessionTime(T51,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))
    		elseif atype == 0x34 then
    			subtree:add(buffer(pos - alen, alen), "  UserAgent(T52,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))
    		elseif atype == 0x35 then
    			subtree:add(buffer(pos - alen, alen), "  InputOctets(T53,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))	
    		elseif atype == 0x36 then
    			subtree:add(buffer(pos - alen, alen), "  OutputOctets(T54,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))	
    		elseif atype == 0x37 then
    			subtree:add(buffer(pos - alen, alen), "  InputPackets(T55,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))	
    		elseif atype == 0x38 then
    			subtree:add(buffer(pos - alen, alen), "  OutputPackets(T56,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))	
    		elseif atype == 0x39 then
    			subtree:add(buffer(pos - alen, alen), "  InputGigawords(T57,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))	
    		elseif atype == 0x3a then
    			subtree:add(buffer(pos - alen, alen), "  OutputGigawords(T58,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))					
			elseif atype == 200 then
    			subtree:add(buffer(pos - alen, alen), "  Servicename(T200,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))
    		elseif atype == 201 then
    			subtree:add(buffer(pos - alen, alen), "  Replymsg(T201,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))
    		elseif atype == 0xf1 then
    			subtree:add(buffer(pos - alen, alen), "  Useripv6(T241,L"..alen.."): "..buffer(pos - alen + 2, alen - 2))
			else
    			subtree:add(buffer(pos - alen, alen), "  Unknown(T"..atype..",L"..alen"): "..buffer(pos - alen + 2, alen - 2))
    		end
    end


    pinfo.cols.info = "cmportal "..type_str.." no="..num..",id="..reqid..",len="..size
end
      
		tcp_table = DissectorTable.get("udp.port")
		--注册到udp端口
		tcp_table:add(2000,cmportal_proto)

