class opt:
    def __init__(self, args):  # args: crt.Arguments; example: 'a=true b,c=1'
        self.o = {}
        s = ""
        if type(args) != str:
            for index in range(args.Count):
                s = s + args[index] + " "
        else:
            s = args
        self.o = parse(s)

    def get(self):
        return self.o

    def getval(self, k):
        return self.o[k] if k in self.o else None

    def getlist(self):
        l = []
        for k, v in self.o.items():
            l.append((k, v))
        return l


def parse(s):
    s = s.replace(",", " ").replace("  ", " ").strip()  # support '[,  ]' as ' '
    pairs = s.split(" ")
    o = {}
    if len(s) == 0:
        return o
    for tv in pairs:
        args = tv.split("=")
        o[args[0]] = args[1] if len(args) >= 2 else True
    return o
