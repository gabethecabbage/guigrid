#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import os
import subprocess
       
def main():
    config_file=open('/home/'+getpass.getuser()+'/.sbgrid.conf', 'r')
    prog_tuples = find_sbgrid_progs() #(ProgramName, [vernums, disable]
    read_config(config_file)
    get_override_name(prog_tuples[20][0])



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
    progs_list = list_top_level_dir(prog_folder)
    progs_list.sort()
    prog_tuples=[]
    for app in progs_list:
        ver_list = list_top_level_dir(prog_folder+app)
        ver_list.sort()
        ver_list.append("disable")
        prog_tuples.append((app,ver_list))
    return prog_tuples
    
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
