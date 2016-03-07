#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import os
import subprocess

    
def open_config():
    """Locates and opens the sbgrid config file, if none is 
    found it opens a default file with only the header"""
    
    conf_path='/home/'+getpass.getuser()+'/.sbgrid.conf'
    if not os.path.isfile(conf_path):
        conf_path='gbsgrid_default.conf'
    
    config_file=open(conf_path, 'r')
    return config_file

def read_config(config_file):
    """Creates 2 arrays, 1 to store the header lines and
    another array of list to store any existing overides.
    New overrides can be added to this array later."""
    
    config_header = []
    config_array = []
    
    for line in config_file:
        s=str(line)
        """look for "#" chars, these indicate header lines, 
	also means comments will be moved above overides"""
        if s[0] == "#": 
            config_header.append(s)
        else:
        #uses "=" to deliniate ProgName from VerNum
            eq_pos = s.find("=")
            config_array.append([s[0:eq_pos],s[eq_pos+1:-1]])
    config_file.close()

    return config_header, config_array

def write_config(config_header, config_array):
    """Backs up old config file to a .bak file,
    writes config header lines, including user comments,
    then writes out each config_array entry as a new line."""

    conf_path='/home/'+getpass.getuser()+'/.sbgrid.conf'
    if os.path.isfile(conf_path+'.bak'): 
		os.remove(conf_path+'.bak')    
    if os.path.isfile(conf_path):
		os.rename(conf_path, conf_path+'.bak')
    config_file=open(conf_path, 'w')
    config_file.writelines(config_header)
    for i in config_array: 
		config_file.write(i[0]+"="+i[1]+"\n")
    config_file.close()
        
def list_top_level_dir(pwd):
    #pythonic ls -d, provides list of dirs in

    dirlist=[ name for name in os.listdir(pwd) if os.path.isdir(os.path.join(pwd, name)) ]
    return dirlist

def detect_branch():
    """Look for an sbgrid installation and detect the OS/Arch in use,
    produces simple distionary with path to branch and platform a suffix"""
    
    branch = {}
    dir_list = list_top_level_dir("/programs/")
    for dir in dir_list:
        if dir == "i386-linux":
            branch['folder'] = "/programs/i386-linux"
            branch['suffix'] = "_L"
        elif dir == "x86_64-linux":
            branch['folder'] = "/programs/x86_64-linux"
            branch['suffix'] = "_X"

        elif dir == "i386-mac":
            branch['folder'] = "/programs/i386-mac"
            branch['suffix'] = "_M"
        elif dir == "powermac":
            branch['folder'] = "/programs/powermac"
            branch['suffix'] = "_P"

    return branch

def find_sbgrid_progs():
    """Searches host file system and makes an alphabetised list,
    ignores any directories without a *.rc file"""

    branch = detect_branch()
    dir_list = list_top_level_dir(branch['folder'])
    prog_list = []
    for dir in dir_list:
        if os.path.isfile(branch['folder']+'/'+dir+'/'+dir+'.rc'):
            prog_list.append(dir)
    prog_list.sort()
    return prog_list
    
def scrape_sbgrid_progs_info(prog_list):
    """Makes a dict with
    prog names as keys leading to a list of versions"""

    branch = detect_branch()
    prog_dict={}
    for prog in prog_list:
        prog_dict[prog]= parse_prog_rc(prog, branch)
    return prog_dict

def parse_prog_rc(prog_name, branch):
    """reads a package rc file and converts this to a dictionary to be 
    queried by either the front or backend"""

    rc_path=branch['folder']+'/'+prog_name+'/'+prog_name+'.rc'

    prog_rc=open(rc_path, 'r')
    verline = -1
    while verline == -1:
        s=prog_rc.readline()
        verline = s.find("setVersion")

    s = s.replace('"','')
    prog_info = {}
    prog_info["overide_name"] = s.split()[1]+branch['suffix']
    prog_info["defver"] = s.split()[2]
    prog_info["otherver"] = []
    for i in range(len(s.split())):
        if i > 2: prog_info["otherver"].append(s.split()[i])

    prog_info["allver"] = prog_info["otherver"]
    prog_info["allver"].insert(0,prog_info["defver"])

    return prog_info
        


def add_override(config_array, prog, ver, prog_dict):
    """checks if a version override already exists for this program, if so it
    edits the old one, if not it adds a new one."""
    
    already_added = False    
    for i in config_array:
        if i[0] == prog_dict[prog]["overide_name"]:
            i[1] = ver
            already_added = True
    if already_added == False:
        config_array.append([prog_dict[prog]["overide_name"],ver])
    return config_array
        
    



if __name__ == '__main__':
    main()

