import os


class DevMapperError(Exception):
    pass


class DevMapper:
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
            DevMapperError('Failed to Access {file}'.format(file=path))

        raise DevMapperError('Unknown Dev Path: {path}'.format(path=path))
