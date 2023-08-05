from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rpi-rf',
    version='0.9.0',
    author='Micha LaQua',
    author_email='micha.laqua@gmail.com',
    description='Sending and receiving 433Mhz signals with cheap GPIO RF Modules a Raspberry Pi',
    long_description=long_description,
    url='https://github.com/milaq/rpi-rf',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=[
        'rpi',
        'raspberry',
        'raspberry pi',
        'rf',
        'gpio',
        'radio',
        '433',
        '433mhz'
    ],
    install_requires=['RPi.GPIO'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
)
