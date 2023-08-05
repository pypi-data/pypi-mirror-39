
import os
import shutil
import unittest

from devmapper.mapper import DevMapper, DevMapperError


class DevMapperSerialTest(unittest.TestCase):
    def setUp(self):
        devname = 'ttyS0'
        devpath = ''
        for root, dirs, files in os.walk('/sys/devices'):
            for dn in dirs:
                if dn == devname:
                    devpath = '/'.join(os.path.join(root, dn).split('/')[:-1])
                    break
        self.devname = '/dev/'+devname
        self.devpath = devpath

    def test_serial_ttyS0_case_1(self):
        # Use: /sys/devices/pnp0/00:08/tty
        devname = DevMapper.serial(self.devpath)
        self.assertEqual(self.devname, devname)

    def test_serial_ttyS0_case_2(self):
        # Use: /sys/devices/pnp0/00:08/tty/
        devname = DevMapper.serial(self.devpath+'/')
        self.assertEqual(self.devname, devname)

    def test_serial_dev_file(self):
        # Use: /dev/ttyS0
        devname = DevMapper.serial(self.devname)
        self.assertEqual(self.devname, devname)

    def test_serial_invalid_path(self):
        try:
            devname = DevMapper.serial('/sys/devices/my/device/path')
        except DevMapperError:
            pass


class DevMapperInterfaceNameTest(unittest.TestCase):
    DIR_TEST = '/tmp/_devices'
    DIR_GOOD = DIR_TEST+'/good/test'
    DIR_BAD = DIR_TEST+'/bad/test'
    DIRS = [DIR_GOOD, DIR_BAD]

    DESC_GOOD_PORT = 'Pseudo Serial Good Port'
    DESC_BAD_PORT = 'Pseudo Serial Bad Port'
    GOOD_PORT = 'ttySerial'

    prepared = False

    def setUp(self):
        for d in self.DIRS:
            if not os.path.exists(d):
                os.makedirs(d)

        if not self.prepared:
            self.prepared = True
            DevMapper.write_one_line(
                    self.DIR_GOOD+'/interface', self.DESC_GOOD_PORT)
            DevMapper.write_one_line(
                    self.DIR_BAD+'/interface', self.DESC_BAD_PORT)
            dpath = self.DIR_GOOD+'/'+self.GOOD_PORT
            if not os.path.exists(dpath):
                os.makedirs(dpath)

    def tearDown(self):
        shutil.rmtree(self.DIR_TEST)

    def test_interface_name_good(self):
        devname = DevMapper.interface_name(
                    self.DESC_GOOD_PORT, base_dir=self.DIR_TEST)
        self.assertEqual(devname, '/dev/'+self.GOOD_PORT)

    def test_interface_name_bad(self):
        exception = False
        try:
            devname = DevMapper.interface_name(
                        self.DESC_BAD_PORT, base_dir=self.DIR_TEST)
        except DevMapperError:
            exception = True
        finally:
            self.assertTrue(exception)
