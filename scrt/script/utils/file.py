def read(name):
    try:
        f = open(name)
        d = f.read()
        f.close()
        return d
    except:
        return ""


def write(name, data):
    f = open(name, "w")
    f.write(data)
    f.close()
