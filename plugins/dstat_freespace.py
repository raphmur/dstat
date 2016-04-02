### Author: Dag Wieers <dag$wieers,com>

### FIXME: This module needs infrastructure to provide a list of mountpoints
### FIXME: Would be nice to have a total by default (half implemented)

class dstat_plugin(dstat):
    """
    Amount of used and free space per mountpoint.
    """

    def __init__(self):
        self.nick = ('used', 'free')
        self.cols = 2

    def vars(self):
        # df has all the currently mounted filesystems
        lines = os.popen("df").read()
        lines = lines.splitlines() # Make a list of the lines
        lines = lines[1:]          # First line is the header we don't need it

        ret = []

        # Loop through what we found and filter out anything with tmpfs in it
        for l in lines:
            parts = l.split()
            ftype = parts[0]
            mount = parts[5]

            # Skip tmpfs and devtmpfs file systems
            if "tmpfs" in ftype:
                continue
            else:
                ret.append(mount)

        return ret

    def name(self):
        return ['/' + os.path.basename(name) for name in self.vars]

    def extract(self):
        self.val['total'] = (0, 0)
        for name in self.vars:
            res = os.statvfs(name)
            self.val[name] = ( (float(res.f_blocks) - float(res.f_bavail)) * long(res.f_frsize), float(res.f_bavail) * float(res.f_frsize) )
            self.val['total'] = (self.val['total'][0] + self.val[name][0], self.val['total'][1] + self.val[name][1])

# vim:ts=4:sw=4:et
