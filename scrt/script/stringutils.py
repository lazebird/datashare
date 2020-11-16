def optparse(s):
	opthash = {}
	s = s.replace("#", " ") # support '#' as ' '
	s = s.replace(",", " ") # support ',' as ' '
	s = s.replace("  ", " ") # support '  ' as ' '
	pairs = s.split(" ")
	for tv in pairs:
		args = tv.split("=")
		if len(args) < 2:
			print "invalid args: ", tv
			continue
		opthash[args[0]] = args[1]
	return opthash
