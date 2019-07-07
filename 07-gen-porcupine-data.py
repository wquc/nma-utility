#--------------------------------------------------------------
# o Generate the nmm files as input of "viz-porcupine-plot.tcl" 
#   to make porcupine plots of protein.
# o The .nmm file has the following format:
#   ATOM $resid $vec_x $vec_y $vec_z
#                                                          Q.W.
#--------------------------------------------------------------

import numpy as np

name_suffix = "_eigenvectors_protein_name-state_name"

def gen_nmm(mode):
# step 1. Read atom name and index
    pdb_name = "pdb_name.charmm_format.pdb"
    vec_name = "mode" + str(mode) + name_suffix + ".dat"
    nmm_name = "mode" + str(mode) + name_suffix + ".nmm"
    atom_x  = []
    atom_id = []
    with open(pdb_name, 'r') as pdb_file:
        atom_count = 0
        for pdb_line in pdb_file:
            if(pdb_line[0:7].strip() == 'ATOM'):
                atom_x.append(pdb_line[0:7].strip())
                atom_id.append(pdb_line[7:12].strip())
                atom_count += 1
    print "%s atoms recorded " % atom_count
# step 2. Read eigenvector of certain mode
    vec_src = np.genfromtxt(vec_name)
    len_of_vec = len(vec_src)
    if(len_of_vec != atom_count):
        print "Error: atom count in pdb file and vector file does not match."
        exit(1)
    vec_x   = vec_src[:,0]
    vec_y   = vec_src[:,1]
    vec_z   = vec_src[:,2]
# step 3. Write data into .nmm file
    with open(nmm_name, 'w') as nmm_file:
        for i in range(0, len_of_vec):
            nmm_file.write('%s  %5d  %12.6f %12.6f %12.6f\n'%(atom_x[i],int(atom_id[i]),vec_x[i],vec_y[i],vec_z[i]))

#usage:
if __name__=="__main__":
    gen_nmm(7)