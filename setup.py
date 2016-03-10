#!/usr/bin/python
from setuptools import setup

from guigrid.gui import __version__ as version


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
        ('/usr/share/icons/hicolor/scalable/apps', ['data/guigrid-icon.svg']),
        ('/usr/share/applications', ['data/guigrid.desktop']),
        ('/etc/skel', ['data/.sbgrid.conf'])
    ],
    entry_points={
        'console_scripts': [
            'guigrid=guigrid.gui:main',
        ],
    },
)
