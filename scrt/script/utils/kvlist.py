class kvlist:
    def __init__(self, s):  # example: "[('nsm', 'reboot'), ('onmd', 'restart'), ('hsl', 'none')]"
        try:
            self.l = eval(s)
        except:
            self.l = []

    def get(self):
        return self.l

    def add(self, k, v):
        index = self.indexof(k)
        if index >= 0:
            del self.l[index]
        self.l.append((k, v))

    def findval(self, k):
        for item in self.l:
            if item[0] == k:
                return item[1]
        return None

    def indexof(self, k):
        for item in self.l:
            if item[0] == k:
                return self.l.index(item)
        return -1

    def lastkey(self):
        if len(self.l) <= 0:
            return None
        return self.l[-1][0]
