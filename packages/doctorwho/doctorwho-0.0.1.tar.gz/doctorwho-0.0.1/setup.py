from setuptools import find_packages, setup

setup(
    name='doctorwho',
    version='0.0.1',
    description='Some funny app!',
    author='Tong',
    author_email='3168095199@qq.com',
    url='https://github.com/tongxiaoting',
    packages = find_packages(exclude=['docs', 'tests*']),
)
