#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import os
import subprocess
       
def main():
    conf_path='/home/'+getpass.getuser()+'/.sbgrid.conf'
    if not os.path.isfile(conf_path):
        conf_path='default_sbgrid.conf'
    
    config_file=open(conf_path, 'r')
    prog_dict, prog_list = find_sbgrid_progs()
    read_config(config_file)
    #get_override_name("eman2")



def read_config(config_file):
    config_header = []; h=0
    config_array = []; a=0
    
    for line in config_file:
        s=str(line)
        if s[0] == "#":
            config_header.append(s)
            h=h+1
        else:
            eq_pos = s.find("=")
            config_array.append([s[0:eq_pos],s[eq_pos+1:-1]])
            a=a+1

#    if len(config_array) == 0:
#        config_array.append(["None", "None"])
    return config_header, config_array

def find_sbgrid_progs():
    prog_folder = "/programs/x86_64-linux/"
    prog_list = list_top_level_dir(prog_folder)
    prog_list.sort()
    prog_dict={}
    for app in prog_list:
        ver_list = list_top_level_dir(prog_folder+app)
        ver_list.sort()
        ver_list.append("disable")
        prog_dict[app]= ver_list
    return prog_dict, prog_list
    
def list_top_level_dir(thedir):            
    dirlist=[ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
    return dirlist

def get_override_name(prog_name):
    arg = "-l "+prog_name
    p = subprocess.Popen(['sbgrid', arg], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    ov_nam=out[out.find('Overrides use this shell variable:')+36:]
    print ov_nam.strip()
    



if __name__ == '__main__':
    main()    
