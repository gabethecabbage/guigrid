#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import os
import subprocess

    
def open_config():
    """Opens the sbgrid config file."""
    conf_path='/home/'+getpass.getuser()+'/.sbgrid.conf'
    #if none is found load a default file with only the header
    if not os.path.isfile(conf_path):
        conf_path='.sbgrid.conf'
    
    config_file=open(conf_path, 'r')
    return config_file

def read_config(config_file):
    """Return array with config header, return array with config lines

    Returns 2 arrays; an array to store the header lines,
    an array to store any existing overides.
    New overrides can be added to latter array later.
    """
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
    """Writes new config files

    Backs up old config file to a .bak file,
    writes config header lines, including user comments,
    then writes out each config_array entry as a new line.
    """
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
        
def ls_dirs(pwd):
    """Returns list of dirs in a given dir"""

    dirlist=[ name for name in os.listdir(pwd) if os.path.isdir(os.path.join(pwd, name)) ]
    return dirlist

def detect_branch():
    """Returns branch dict with folder and suffix keys

    Looks for an sbgrid installation and detect the OS/Arch in use,
    produces simple distionary with path to branch and platform a suffix
    """
    branch = {}
    dir_list = ls_dirs("/programs/")
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

def ls_progs(path):
    """Return list of installed SBgrid programs

    Searches a path for folders with a *.rc file,
    places these in an alphabetised list
    """
    dir_list = ls_dirs(path)
    progs_list = []
    for dir in dir_list:
        """only if the program has an *.rc file, should we index it.
        those without likely have no versioning or override information"""
        if os.path.isfile(path+'/'+dir+'/'+dir+'.rc'):
            progs_list.append(dir)
    progs_list.sort()
    return progs_list
    
def scrape_all_progs(branch, progs_list):
    """Returns dict with program name as key and dicts of info as entries

    Iterates through a list of programs, searches a proveded branch for
    each programs .rc file. The .rc file is parsed to extract version 
    information and override names. The .rc info is placed in a dictionary,
    stored in another ditionary using program names as keys.
    """
    progs_dict={}
    #read a packages rc file and convert to a dictionary
    for prog_name in progs_list:
        rc_path=branch['folder']+'/'+prog_name+'/'+prog_name+'.rc'

        prog_rc=open(rc_path, 'r')
        #look for the version control metadata line starting with "setVersion"
        is_ver_line = -1
        while is_ver_line == -1:
            current_line=prog_rc.readline()
            is_ver_line = current_line.find("setVersion")
        set_ver_ls = current_line.replace('"','').split()
        
        prog_info = {}
        #2nd item on line is the override name
        prog_info["override_name"] = set_ver_ls[1]+branch['suffix']
        #3rd item on line is the default version
        prog_info["defver"] = set_ver_ls[2]
        #remaining items are all other versions
        prog_info["otherver"] = []
        for i in range(len(set_ver_ls)):
            if i > 2: 
                prog_info["otherver"].append(set_ver_ls[i])
        prog_info["otherver"].append("disable")

        #combine default vers and other vers for complete with default at start
        prog_info["allver"] = prog_info["otherver"]
        prog_info["allver"].insert(0,prog_info["defver"])

        progs_dict[prog_name]= prog_info
        prog_rc.close()

    return progs_dict

def add_override(config_array, prog, ver, prog_dict):
    """Returns modified config_array with an override updated

    Check if a version override already exists for this program, if yes,
    edit the old one, if no, add new one.
    """
    already_added = False    
    for i in config_array:
        if i[0] == prog_dict[prog]["override_name"]:
            i[1] = ver
            already_added = True
    if already_added == False:
        config_array.append([prog_dict[prog]["override_name"],ver])
    return config_array


if __name__ == '__main__':
    main()

