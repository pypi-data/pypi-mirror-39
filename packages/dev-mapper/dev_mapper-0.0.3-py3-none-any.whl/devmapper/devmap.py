#!/usr/bin/env python

from __future__ import print_function

import sys

from functools import partial

from devmapper.mapper import DevMapperError, DevMapper



ERR = partial(print, file=sys.stderr)
DEV_MAP = {
    'serial':   DevMapper.serial,
}


def mapper(mode, path):
    if DEV_MAP.get(mode, None) is None:
        usage()
        raise DevMapperError('Not Supported mode: {mode}.'.format(mode=mode))

    return DEV_MAP.get(mode)(path)


def usage():
    '''  Usage: devmap.py <mode> <sys-device-pci-address>
    mode:
        serial      - convert sys-device-pci-address to /dev/ttyXXX.
'''
    ERR(usage.__doc__)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
        raise DevMapperError('Not Enough Parameters')

    mode = sys.argv[1]
    dpath = sys.argv[2]
    print(mapper(mode, dpath), end='')
