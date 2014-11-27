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
        conf_path='default_sbgrid.conf'
    
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
        #look for #, these indicate header lines, also means comments will be moved above overides
        if s[0] == "#": 
            config_header.append(s)
        else:
        #uses = to deliniate ProgName from VerNum
            eq_pos = s.find("=")
            config_array.append([s[0:eq_pos],s[eq_pos+1:-1]])
    config_file.close()

#    if len(config_array) == 0:
#        config_array.append(["None", "None"])
    return config_header, config_array

def write_config(config_header, config_array):
    conf_path='/home/'+getpass.getuser()+'/.sbgrid.conf'
    if os.path.isfile(conf_path+'.bak'): os.remove(conf_path+'.bak')    
    os.rename(conf_path, conf_path+'.bak')
    config_file=open(conf_path, 'w')    
    config_file.writelines(config_header)
    for i in config_array: config_file.write(i[0]+"="+i[1]+"\n")
    config_file.close()
        
    

def find_sbgrid_progs():
    """Searches host file system and lists all installed sbgrid software,
    makes an alphabetical list for easy browsing and a dict with
    prog names as keys leading to a list of versions"""

    prog_folder = "/programs/x86_64-linux/" #here thar be binaries
    prog_list = list_top_level_dir(prog_folder)
    prog_list.sort()
    prog_dict={}
    for prog in prog_list:
        ver_list = list_top_level_dir(prog_folder+prog)
        ver_list.sort()
        ver_list.append("disable") #not actually a version but it allows for disabling a package
        prog_dict[prog]= ver_list
    return prog_dict, prog_list
    
def list_top_level_dir(thedir):
    """just ls -d in python form, dumps output to list"""
    dirlist=[ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
    return dirlist

def get_override_name(prog_name):
    """call out to the sbgrid command that gives the override name for packages,
    although it is normally just all upper case with _X on the end"""
    arg = "-l "+prog_name
    p = subprocess.Popen(['sbgrid', arg], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    ov_nam=out[out.find('Overrides use this shell variable:')+36:]
    return ov_nam.strip()

def add_override(config_array, prog, ver):
    """checks if a version override already exists for this program, if so it
    edits the old one, if not it adds a new one."""
    already_added = False    
    for i in config_array:
        if i[0] == get_override_name(prog):
            i[1] = ver
            already_added = True
    if already_added == False:
        config_array.append([get_override_name(prog),ver])
    return config_array
        
    



if __name__ == '__main__':
    main()    
