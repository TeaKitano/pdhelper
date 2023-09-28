from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name='pdhelper',
    version='0.1.0',
    license='BSD 3-Clause License',
    description='Useful pandas helper',
    author='TeaKitano',
    author_email='chachamusics@outlook.com',
    packages=["pdhelper"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["pandas","openpyxl"]
)
