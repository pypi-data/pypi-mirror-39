# Python wrapper for the rpi_vl53l0x library.
# Author: Peter Yang (turmary@126.com)
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages, Extension
from setuptools.command.build_py import build_py
import subprocess

class CustomInstallCommand(build_py):
    """Customized install to run library Makefile"""
    def run(self):
        print("Compiling vl53l0x library...")
        proc = subprocess.Popen(["make", "-C", ".."], \
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(proc.stderr.read())
        build_py.run(self)


setup(name              = 'rpi_vl53l0x',
      version           = '0.0.1',
      author            = 'Peter Yang <turmary@126.com>',
      author_email      = 'turmary@126.com',
      description       = 'Userspace Raspberry Pi VL53l0X library',
      license           = 'MIT',
      url               = 'https://github.com/turmary/rpi-vl53l0x',
      cmdclass          = {'build_py':CustomInstallCommand},
      # packages          = ['rpi_vl53l0x'],
      py_modules        = ['vl53l0x_api'],
      ext_modules       = [Extension('_rpi_vl53l0x', 
                                     include_dirs=['../platform/inc', '../VL53L0X_1.0.2/Api/core/inc'],
                                     sources=['rpi_vl53l0x.i'],
                                     library_dirs=['../.', '../bin'],
                                     libraries=['vl53l0x', 'rt'])])

