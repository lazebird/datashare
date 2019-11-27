-- 定义协议，可以在wireshark中使用bcmp_frame过滤
bcmp_frame_proto = Proto("bcmp_frame","bcmp_frame","bcmp_frame Protocol")

function bcmp_frame_get_pkttypestr(type)
	pkttypestr = {[1]="REG", [2]="TICK", [3]="RES", [4]="PARACHG"}
	return pkttypestr[type] or "Unknown"
end

function bcmp_frame_get_devtypestr(type)
	devtypestr = {[2]="CBAT_HS", [3]="ONU", [4]="ENTITY"}
	return devtypestr[type] or "Unknown"
end

datapos = 0
function addint(subtree, buffer, name, len)
	value = buffer(datapos,len):uint()
	subtree:add(buffer(datapos,len), name.. value)
	datapos = datapos + len
	return value
end
function addstring(subtree, buffer, name, len)
	subtree:add(buffer(datapos,len), name.. buffer(datapos,len):string())
	datapos = datapos + len
end
function addipv4(subtree, buffer, name)
	subtree:add(buffer(datapos,4), name.. tostring(buffer(datapos,4):ipv4()))
	datapos = datapos + 4
end
function addether(subtree, buffer, name)
	subtree:add(buffer(datapos,6), name.. tostring(buffer(datapos,6):ether()))
	datapos = datapos + 6
end
function adddata(subtree, buffer, name, len)
	subtree:add(buffer(datapos,len), name.. buffer(datapos,len))
	datapos = datapos + len
end
function addtitle(subtree, buffer, name, len)
	subtree:add(buffer(datapos,len), name)
end
function adddevtype(subtree, buffer, name)
	subtree:add(buffer(datapos,1), name.. bcmp_frame_get_devtypestr(buffer(datapos,1):uint()))
	datapos = datapos + 1
end
function addpkttype(subtree, buffer, name)
	type = buffer(datapos,1):uint()
	type = bit32.rshift(type, 4)
	subtree:add(buffer(datapos,1), name.. bcmp_frame_get_pkttypestr(type))
	datapos = datapos + 1
	return type
end
function addver(subtree, buffer, name)
	ver = buffer(datapos,1):uint()
	majorver = bit32.rshift(ver, 4)
	minorver = bit32.band(ver, 0xf)
    subtree:add(buffer(datapos,1),name  .. majorver.."."..minorver)
	datapos = datapos + 1
end

function bcmp_ip_resolve_reg(subtree, buffer, datalen)
	addtitle(subtree, buffer, "Layer 1:", datalen)
	addint(subtree, buffer, "  Length: ", 1)
	adddevtype(subtree, buffer, "  Device: ")
	addether(subtree, buffer, "  MAC: ")
	if datalen == 32 then
		addint(subtree, buffer, "  Port ID: ", 4)
		addether(subtree, buffer, "  ONU MAC: ")
	end
	addint(subtree, buffer, "  ONU ID: ", 4)
	addint(subtree, buffer, "  OLT ID: ", 4)
	addint(subtree, buffer, "  SLOT ID: ", 4)
	adddata(subtree, buffer, "  Padding: ", 2)
end

function bcmp_ip_resolve_tick(subtree, buffer, datalen)
	addtitle(subtree, buffer, "Layer 1:", datalen)
	addint(subtree, buffer, "  Length: ", 1)
	adddevtype(subtree, buffer, "  Device: ")
	addether(subtree, buffer, "  MAC: ")
	addint(subtree, buffer, "  Mgmt param id: ", 2)
	if datalen == 32 then
		addint(subtree, buffer, "  Port ID: ", 4)
		addether(subtree, buffer, "  ONU MAC: ")
	end
	addint(subtree, buffer, "  ONU ID: ", 4)
	addint(subtree, buffer, "  OLT ID: ", 4)
	addint(subtree, buffer, "  SLOT ID: ", 4)
end

function bcmp_ip_resolve_res(subtree, buffer, datalen)
	addtitle(subtree, buffer, "Layer 1:", datalen)
	addint(subtree, buffer, "  Length: ", 1)
	adddevtype(subtree, buffer, "  Device: ")
	
	--adddata(subtree, buffer, "  Mgmt IP: ", 16)
	adddata(subtree, buffer, "  Padding: ", 12)
	addipv4(subtree, buffer, "  Mgmt IP: ")
	
	addipv4(subtree, buffer, "  IP Mask: ")
	
	--adddata(subtree, buffer, "  Gateway: ", 16)
	adddata(subtree, buffer, "  Padding: ", 12)
	addipv4(subtree, buffer, "  Gateway: ")
	
	addint(subtree, buffer, "  Mgmt VID: ", 2)
	addint(subtree, buffer, "  SNMP ver.: ", 1)
	addint(subtree, buffer, "  SNMP port: ", 2)
	addstring(subtree, buffer, "  SNMP Secname: ", 32)
	addstring(subtree, buffer, "  SNMP read community: ", 32)
	addstring(subtree, buffer, "  SNMP write community: ", 32)
	addint(subtree, buffer, "  Heartbeat cycle: ", 2)
	addint(subtree, buffer, "  Mgmt param id: ", 2)
	addstring(subtree, buffer, "  IP assign time: ", 12)
	addipv4(subtree, buffer, "  OLT IP: ")
end

function bcmp_ip_resolve_unknown(subtree, buffer, datalen)
	addtitle(subtree, buffer, "Layer 1:", datalen)
	addint(subtree, buffer, "  Length: ", 1)
	adddevtype(subtree, buffer, "  Device: ")
	adddata(subtree, buffer, "  Data: ", datalen - 2)
end

function bcmp_frame_resolve_reg(subtree, buffer, layernum)
	addtitle(subtree, buffer, "Layer 1:", buffer(datapos,1):uint())
	addint(subtree, buffer, "  Length: ", 1)
	adddevtype(subtree, buffer, "  Device: ")
	addether(subtree, buffer, "  MAC: ")
	if layernum > 1 then
		addtitle(subtree, buffer, "Layer 2:", buffer(datapos,1):uint())
		addint(subtree, buffer, "  Length: ", 1)
		adddevtype(subtree, buffer, "  Device: ")
		addint(subtree, buffer, "  Portid: ", 4)
		adddata(subtree, buffer, "  Padding: ", 2)
	end
end

function bcmp_frame_resolve_tick(subtree, buffer, layernum)
	layerlen = buffer(datapos,1):uint()
	addtitle(subtree, buffer, "Layer 1:", layerlen)
	addint(subtree, buffer, "  Length: ", 1)
	adddevtype(subtree, buffer, "  Device: ")
	addether(subtree, buffer, "  MAC: ")
	addint(subtree, buffer, "  Mgmt param id: ", 2)
	adddata(subtree, buffer, "  Padding: ", 2)
	if layernum > 1 then
		addtitle(subtree, buffer, "Layer 2:", buffer(datapos,1):uint())
		addint(subtree, buffer, "  Length: ", 1)
		adddevtype(subtree, buffer, "  Device: ")
		addint(subtree, buffer, "  Portid: ", 4)
		adddata(subtree, buffer, "  Padding: ", 2)
	end
end

function bcmp_frame_resolve_res(subtree, buffer, layernum)
	datalen = buffer(datapos,1):uint()
	bcmp_ip_resolve_res(subtree, buffer, datapos, datalen)
end

function bcmp_frame_resolve_unknown(subtree, buffer, layernum)
	for i = 1, layernum do
		layerlen = buffer(datapos,1):uint()
		addtitle(subtree, buffer, "Layer "..i..":", layerlen)
		addint(subtree, buffer, "  Length: ", 1)
		adddevtype(subtree, buffer, "  Device: ")
		adddata(subtree, buffer, "  Data: ", layerlen - 2)
	end
end

framemap = {}
framemap["Unknown"] = bcmp_frame_resolve_unknown
framemap["REG"] = bcmp_frame_resolve_reg
framemap["TICK"] = bcmp_frame_resolve_tick
framemap["RES"] = bcmp_frame_resolve_res
framemap["PARACHG"] = bcmp_frame_resolve_res
ipmap = {}
ipmap["Unknown"] = bcmp_ip_resolve_unknown
ipmap["REG"] = bcmp_ip_resolve_reg
ipmap["TICK"] = bcmp_ip_resolve_tick
ipmap["RES"] = bcmp_ip_resolve_res
ipmap["PARACHG"] = bcmp_ip_resolve_res

-- dissector函数
function bcmp_frame_proto.dissector(buffer,pinfo,tree)
   
    --pinfo的成员可以参考用户手册
    pinfo.cols.protocol = "bcmp_frame"
   
    local subtree = tree:add(bcmp_frame_proto,buffer(),"bcmp_frame Protocol")
			
	datapos = 0
	addtitle(subtree, buffer, "Header: ", 16)
	addver(subtree, buffer, "  Version: ")
 	type = addpkttype(subtree, buffer, "  Type: ")
	addint(subtree, buffer, "  Seq: ", 2)
	addint(subtree, buffer, "  Checksum: ", 2)
	addint(subtree, buffer, "  Length: ", 2)
	layernum = addint(subtree, buffer, "  Layers number: ", 2)
	adddata(subtree, buffer, "  Padding: ", 6)
	framemap[bcmp_frame_get_pkttypestr(type)](subtree, buffer, layernum)
end

eth_table = DissectorTable.get("ethertype") --eth.type == 0x0877
eth_table:add(0x0877,bcmp_frame_proto)


-- 定义协议，可以在wireshark中使用bcmp_ip过滤
bcmp_ip_proto = Proto("bcmp_ip","bcmp_ip","bcmp_ip Protocol")

-- dissector函数
function bcmp_ip_proto.dissector(buffer,pinfo,tree)
   
    --pinfo的成员可以参考用户手册
    pinfo.cols.protocol = "bcmp_ip"
   
    local subtree = tree:add(bcmp_ip_proto,buffer(),"bcmp_ip Protocol")
			
	datapos = 0
	addtitle(subtree, buffer, "Header: ", 20)
	addver(subtree, buffer, "  Version: ")
 	type = addpkttype(subtree, buffer, "  Type: ")
	addint(subtree, buffer, "  Seq: ", 2)
	addint(subtree, buffer, "  Checksum: ", 2)
	len = addint(subtree, buffer, "  Length: ", 2)
	addether(subtree, buffer, "  Client MAC: ")
	adddata(subtree, buffer, "  Padding: ", 6)
	ipmap[bcmp_frame_get_pkttypestr(type)](subtree, buffer, (len-20))
end

udp_table = DissectorTable.get("udp.port") --udp.port == 5000
--注册到udp
udp_table:add(5000,bcmp_ip_proto)
