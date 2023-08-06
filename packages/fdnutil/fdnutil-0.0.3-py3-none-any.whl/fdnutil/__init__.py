import re
def chunk(dlist:list, n:int ):
    for i in range(0,len(dlist), n):
            yield dlist[i: i+n]

class Connection:
    def __init__(self, dsn):
        print("dsn is : ", dsn)
        # rx = re.compile(pattern)
        m = re.search(r"(?P<driver>\w)://(?P<uname>\w+):(?P<pwd>\w+)@(?P<host>\w+)/(?P<db>\w+)", dsn)
        self.username = m.group('uname')
        self.password = m.group('pwd')
        self.host = m.group('host')
        self.db = m.group('db')
