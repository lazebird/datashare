timeout = 5
portnum = 10
llidperport = 30
macfmt = "0000.0000.0000"
ret = 4
for (i = 1 i <= portnum and ret > 3 i+=1) 
	crt.Screen.Send("interface epon0/"+i+"\n")
	for (j = 0 j < llidperport and ret > 3 j+=1) 
		macpost = (i + j * llidperport).toString()
		mac = macfmt.substr(0, macfmt.length - macpost.length) + macpost
		crt.Screen.Send(" onu bind mac-address " + mac + " llid "+j+"\n")
		ret = crt.Screen.WaitForStrings(["^C", "<INTERRUPT>", "^Z", "#"], int(timeout))
	
	crt.Screen.Send("exit\n")

crt.Screen.Send("#ret "+ret+"\n")
