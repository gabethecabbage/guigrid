#!/usr/bin/python
from setuptools import setup

from guigrid.main import __version__ as version


with open('README.md') as fh:
    long_description = fh.read()


setup(
    name='guigrid',
    version=version,
    description='SBGrid Program Version Manager',
    long_description=long_description,
    author='Gabe Schrecker',
    author_email='gabriel.schrecker@postgrad.man.ac.uk',
    url='http://octavia.smith.man.ac.uk/PBRB_Gabe/guigrid/tree/master',
    license='GPLv3',
    packages=['guigrid'],
    data_files=[
        ('share/icons/hicolor/scalable/apps', ['data/guigrid-icon.svg']),
        ('share/applications', ['data/guigrid.desktop'])
    ],
    entry_points={
        'console_scripts': [
            'guigrid=guigrid.gui:main',
        ],
    },
)
