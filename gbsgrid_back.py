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
    if os.path.isfile(conf_path+'.bak'): 
	os.remove(conf_path+'.bak')    
    if os.path.isfile(conf_path): 
	os.rename(conf_path, conf_path+'.bak')
    config_file=open(conf_path, 'w')    
    config_file.writelines(config_header)
    for i in config_array: 
	config_file.write(i[0]+"="+i[1]+"\n")
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

"""Doesn't work when run from anything but a terminal, was nice but sadly broken"""
#def get_override_name(prog_name):
#    """call out to the sbgrid command that gives the override name for packages,
#    although it is normally just all upper case with _X on the end"""
#    arg = "-l "+prog_name
#    p = subprocess.Popen(['sbgrid', arg], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#    out, err = p.communicate()
#    ov_nam=out[out.find('Overrides use this shell variable:')+36:]
#    return ov_nam.strip()

def get_override_name(prog_name):
    """Just a big static dict with all the relevant names stored, dumb but working solution
    maybe I'll fix it when I can be bothered. This replicates the func above though."""
    override_dict = {'priism': 'PRIISM_X', 'vmd': 'VMD_X', 'probe': 'PROBE_X', 'xmipp': 'XMIPP_X', 'scc': 'SCC_X', 'graphviz': 'GRAPHVIZ_X', 'threader': 'THREADER_X', 'xdsi': 'XDSI_X', 'iplt': 'IPLT_X', 'bbhp': 'BBHP_X', 'emboss': 'EMBOSS_X', 'remediator': 'REMEDIATOR_X', 'unio': 'UNIO_X', 'ambertools': 'AMBERTOOLS_X', 'rosetta': 'ROSETTA_X', 'sparky': 'SPARKY_X', 'redcat': 'REDCAT_X', 'zdock': 'ZDOCK_X', 'ruby': 'RUBY_X', 'bnp': 'BNP_X', 'pytom': 'PYTOM_X', 'imp': 'IMP_X', 'xds-viewer': 'XDSVIEWER_X', 'clustal': 'CLUSTAL_X', 'xeasy': 'XEASY_X', 'ccpnmr': 'CCPNMR_X', 'nucplot': 'NUCPLOT_X', 'surfnet': 'SURFNET_X', 'main': 'MAIN_X', 'elves': 'ELVES_X', 'electra': 'ELECTRA_X', 'netblast': 'NETBLAST_X', 'em2em': 'EM2EM_X', 'nmrpipe': 'NMRPIPE_X', 'x3d': 'X3D_X', 'xdsstat': 'XDSSTAT_X', 'coot': 'COOT_X', 'python': 'PYTHON_X', 'untangle': 'UNTANGLE_X', 'zephyr': 'ZEPHYR_X', 'autodock': 'AUTODOCK_X', 'dock': 'DOCK_X', 'urox': 'UROX_X', 'xds': 'XDS_X', 'ssaha2': 'SSAHA2_X', 'gefrealign': 'GEFREALIGN_X', 'finchtv': 'FINCHTV_X', 'namd': 'NAMD_X', 'blast': 'BLAST_X', 'ghostscript': 'GHOSTSCRIPT_X', 'dps': 'DPS_X', 'particle': 'PARTICLE_X', 'apbs': 'APBS_X', 'gorgon': 'GORGON_X', 'simulaid': 'SIMULAID_X', 'whatif': 'WHATIF_X', 'mead': 'MEAD_X', 'fastmodelfree': 'FASTMODELFREE_X', 'mafft': 'MAFFT_X', 'psipred': 'PSIPRED_X', 'a2ps': 'A2PS_X', 'jalview': 'JALVIEW_X', 'sharp': 'SHARP_X', 'imagej': 'IMAGEJ_X', 'staden': 'STADEN_X', 'quilt': 'QUILT_X', 'procheck': 'PROCHECK_X', 'modelfree': 'MODELFREE_X', 'rnamlview': 'RNAMLVIEW_X', 'rasmol': 'RASMOL_X', 'spider': 'SPIDER_X', 'crop': 'CROP_X', 'hbplus': 'HBPLUS_X', 'pyrosetta': 'PYROSETTA_X', 'naccess': 'NACCESS_X', 'embfactor': 'EMBFACTOR_X', 'cpmgfit': 'CPMGFIT_X', 'rcsbtools': 'RCSBTOOLS_X', 'ligplus': 'LIGPLUS_X', 'qnifft': 'QNIFFT_X', 'diffmap': 'DIFFMAP_X', 'eman': 'EMAN_X', 'arp_warp': 'ARPWARP_X', 'csrosetta': 'CSROSETTA_X', 'matt': 'MATT_X', 'molphy': 'MOLPHY_X', 'mrtailor': 'MRTAILOR_X', 'cns': 'CNS_X', 'eman2': 'EMAN2_X', 'haddock': 'HADDOCK_X', 'phoelix': 'PHOELIX_X', 'xv': 'XV_X', 'spire': 'SPIRE_X', 'pdb2pqr': 'PDB2PQR_X', 'mes': 'MES_X', 'bsoft': 'BSOFT_X', 'veda': 'VEDA_X', 'caver': 'CAVER_X', 'suprim': 'SUPRIM_X', 'molmol': 'MOLMOL_X', 'autoproc': 'AUTOPROC_X', 'mosflm': 'MOSFLM_X', 'mmtsb': 'MMTSB_X', 'imagemagick': 'IMAGEMAGIC_X', 'aline': 'ALINE_X', 'espript': 'ESPRIPT_X', 'theseus': 'THESEUS_X', 'spdbv': 'SPDBV_X', 'promals': 'PROMALS_X', 'modeller': 'MODELLER_X', 'como': 'COMO_X', 'tcoffee': 'TCOFFEE_X', 'avogadro': 'AVOGADRO_X', 'probcons': 'PROBCONS_X', 'cara': 'CARA_X', 'mmc': 'MMC_X', 'hydropro': 'HYDROPRO_X', 'rmeasure': 'RMEASURE_X', 'cmview': 'CMVIEW_X', 'auto3dem': 'AUTO3DEM_X', 'frealign': 'FREALIGN_X', 'buster': 'BUSTER_X', 'plotmtv': 'PLOTMTV_X', 'yup': 'YUP_X', 'phylip': 'PHYLIP_X', 'bfactor': 'BFACTOR_X', 'openbabel': 'OPENBABEL_X', 'crystfel': 'CRYSTFEL_X', 'rsref2000': 'RSREF2000_X', 'stamp': 'STAMP_X', 'ctf': 'CTF_X', 'mifit': 'MIFIT_X', 'signature': 'SIGNATURE_X', 'raster3d': 'RASTER3D_X', 'gamma': 'GAMMA_X', 'madbend': 'MADBEND_X', 'vina': 'VINA_X', 'aria': 'ARIA_X', 'molscript': 'MOLSCRIPT_X', 'hkl': 'HKL2000_X', 'nedit': 'NEDIT_X', 'dino': 'DINO_X', 'wasp': 'WASP_X', 'pdb-care': 'PDBCARE_X', 'isthms': 'ISTHMS_X', 'balbes': 'BALBES_X', 'pft3dr': 'PFT3DR_X', 'profphd': 'PROFPHD_X', 'dyndom': 'DYNDOM_X', 'raw': 'RAW_X', 'xdsgui': 'XDSGUI_X', 'fiji': 'FIJI_X', 'bobscript': 'BOBSCRIPT_X', 'lafire': 'LAFIRE_X', 'curvesplus': 'CURVESPLUS_X', 'phenix': 'PHENIX_X', 'perl': 'PERL_X', 'pgplot': 'PGPLOT_X', 'pdb_redo': 'PDB_REDO_X', 'talosn': 'TALOSN_X', 'povray': 'POVRAY_X', 'specview': 'SPECVIEW_X', 'raspnmr': 'RASPNMR_X', 'qpack': 'QPACK_X', 'hydronmr': 'HYDRONMR_X', 'surfrace': 'SURFRACE_X', 'refmac': 'REFMAC_X', 'relax': 'RELAX_X', 'reduce': 'REDUCE_X', 'norma': 'NORMA_X', 'mammoth-mult': 'MAMMOTHMULT_X', 'dowser': 'DOWSER_X', 'relion': 'RELION_X', 'module': 'MODULE_X', 'ccp4mg': 'CCP4MG_X', 'hole': 'HOLE_X', 'nuccyl': 'NUCCYL_X', 'grace': 'GRACE_X', 'entangle': 'ENTANGLE_X', 'pipe2xeasy': 'PIPE2XEASY_X', 'solvate': 'SOLVATE_X', 'tiltpicker': 'TILTPICKER_X', 'eden': 'EDEN_X', 'acemd': 'ACEMD_X', 'protskin': 'PROTSKIN_X', 'imosflm': 'IMOSFLM_X', 'concoord': 'CONCOORD_X', 'gromacs': 'GROMACS_X', 'r': 'R_X', 'saxsview': 'SAXSVIEW_X', 'blastplus': 'BLASTPLUS_X', 'dynamo': 'DYNAMO_X', 'emip': 'EMIP_X', 'ccp4': 'CCP4_X', 'somore': 'SOMORE_X', 'ultrascan': 'ULTRASCAN_X', 'situs': 'SITUS_X', 'mgltools': 'MGLTOOLS_X', 'prospect': 'PROSPECT_X', 'rmerge': 'RMERGE_X', 'rnaview': 'RNAVIEW_X', 'sam': 'SAM_X', 'resmap': 'RESMAP_X', 'aqua': 'AQUA_X', 'curves': 'CURVES_X', 'xplor': 'XPLOR_X', 'breseq': 'BRESEQ_X', 'plotutils': 'PLOTUTIL_X', 'chimera': 'CHIMERA_X', 'o': 'O_X', 'knuspr': 'KNUSPR_X', 'whatcheck': 'WHATCHECK_X', 'pymol': 'PYMOL_X', 'fasta': 'FASTA_X', 'ilastik': 'ILASTIK_X', 'simple': 'SIMPLE_X', 'nmrview': 'NMRVIEW_X', 'scwrl3': 'SCWRL3_X', 'amigos2': 'AMIGOS2_X', 'primer3': 'PRIMER3_X', 'epmr': 'EPMR_X', 'imod': 'IMOD_X', 'tkdiff': 'TKDIFF_X', 'wattos': 'WATTOS_X', '2dx': 'A2DX_X', 'mole': 'MOLE_X', 'xdrawchem': 'XDRAWCHEM_X', 'dyndom3d': 'DYNDOM3D_X', 'adxv': 'ADXV_X', 'tcltk': 'TCLTK_X', 'ribbons': 'RIBBONS_X', 'pales': 'PALES_X', 'tensor': 'TENSOR_X', 'ligplot': 'LIGPLOT_X', 'appion': 'APPION_X', 'snb': 'SNB_X', 'igv': 'IGV_X', 'pdbstat': 'PDBSTAT_X', 'mcce': 'MCCE_X', 'phases': 'PHASES_X', 'surfv': 'SURFV_X', 'protomo': 'PROTOMO_X', 'replace': 'REPLACE_X', 'fpocket': 'FPOCKET_X', 'ace2': 'ACE2_X', 'r2r': 'R2R_X', 'geneious': 'GENEIOUS_X', 'pymmlib': 'PYMMLIB_X', 'gnuplot': 'GNUPLOT_X', 'nessy': 'NESSY_X', 'xia2': 'XIA2_X', 'scwrl4': 'SCWRL4_X', '3dna': 'X3DNA_X', 'ringer': 'RINGER_X', 'profit': 'PROFIT_X', 'xdsme': 'XDSME_X', 'solve': 'SOLVE_X', 'alscript': 'ALSCRIPT_X', 'gerard': 'GERARD_X', 'xrayview': 'XRAYVIEW_X', 'amps': 'AMPS_X', 'muscle': 'MUSCLE_X', 'dssr': 'DSSR_X', 'dssp': 'DSSP_X', 'mrc': 'MRC_X'}
    return override_dict[prog_name]

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
