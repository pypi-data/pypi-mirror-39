import os


class DevMapperError(Exception):
    pass


class FileOperate:

    @classmethod
    def read_first_line(cls, fpath, strip=True):
        with open(fpath, "r") as fd:
            for line in fd:
                if line:
                    return line.strip() if strip else line

    @classmethod
    def write_one_line(cls, fpath, string, strip=True):
        with open(fpath, 'w') as fd:
            for line in string.splitlines():
                if line:
                    return fd.write(line.strip() if strip else line)


class DevMapper(FileOperate):
    DEBUG       = False
    SERIAL_PORT = ['ttyS', 'ttyUSB', 'ttyACM']

    @classmethod
    def serial(cls, path, prefix=SERIAL_PORT):
        if path.find('/dev/') == 0:
            return path
        try:
            for dev in os.listdir(path):
                for pfname in prefix:
                    if dev.find(pfname) == 0:
                        return '/dev/'+dev
        except OSError:
            DevMapperError('Failed to Access: {file}'.format(file=path))

        raise DevMapperError('Unknown Dev Path: {path}'.format(path=path))

    @classmethod
    def interface_name(cls, ifname, base_dir='/sys/devices/'):
        ifname = ifname.strip()
        for root, dirs, files in os.walk(base_dir):
            for fn in files:
                if fn == 'interface':
                    fpath = os.path.join(root, fn)
                    dpath = '/'.join(fpath.split('/')[:-1])
                    ifvalue = cls.read_first_line(fpath)
                    if ifname == ifvalue:
                        if cls.DEBUG:
                            print(fpath)
                            print(dpath)
                        return cls.serial(dpath)
        raise DevMapperError('Not Found Interface Name: {}'.format(ifname))
