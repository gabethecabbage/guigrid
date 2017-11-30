

# GUIGrid

**GUIGrid is a gui tool to control the versions of SBGrid managed software.**

![](http://octavia.smith.man.ac.uk/PBRB_Gabe/guigrid/raw/master/data/screenshot.png)

This software is designed to make it easier for average users control their SBgrid software versions in use.

It parses the ~/.sbgrid.conf file to populate a table view with the current settings. It also parses each programs .rc file to get its override name and versions available. 

Once the desired program versions have been selected, the changes can be saved to the ~/.sbgrid.conf file. **These changes will take effect upon starting a new terminal**.

## Dependencies
This software requires that one branch of SBgrid is installed in, or symlinked to, "/programs". 

It is written in Python 3 and PyQt4. These can be installed through your package manager:
e.g. for RHEL:
```bash
yum install PyQt4
```
or for DEB:
```bash
apt-get install python-qt4
```

## Installation
Clone the repo from our gitlab and install using python setuptools.

```bash
git clone https://github.com/gabethecabbage/guigrid.git
cd guigrid
sudo python setup.py install
```


## To do
This software is not yet complete. Desired features and changes are listed below.

1. Test and fix on Ubuntu
1. ~~Add IOError handling~~
1. ~~Clean up backend name space~~
1. ~~Document front end functions~~
1. ~~Use OS native icons~~
1. Make front end layout less static
1. ~~Add tooltips to front end~~
1. ~~Fill this README.md~~
1. ~~Add a setup.py/make system~~

It is untested on Mac OSX installations but should work with minimal modifications. I'm happy to help port the software if there is a demand but I don't have a Mac to test it on.

