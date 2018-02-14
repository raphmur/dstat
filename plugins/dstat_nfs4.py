### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'nfs4 client'
        self.nick = ('read', 'writ', 'rdir', 'othr', 'cmmt')
        self.vars = ('read', 'write', 'readdir', 'other', 'commit')
        self.type = 'd'
        self.width = 5
        self.scale = 1000
        self.open('/proc/net/rpc/nfs')

    def extract(self):
        for l in self.splitlines():
            if not l or l[0] != 'proc4': continue
            self.set2['read'] = long(l[3])
            self.set2['write'] = long(l[4])
            self.set2['readdir'] = long(l[31])
            self.set2['commit'] = long(l[5])
            self.set2['other'] = sum(map(long, l[1:])) - self.set2['read'] - self.set2['write'] - self.set2['readdir'] - self.set2['commit']

        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
