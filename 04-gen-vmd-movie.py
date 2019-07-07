#----------------------------------------------------------
# Generate a PDB file of a series of snapshots of a protein
# along the eigenvector provided.
#                                                      Q.W.
#----------------------------------------------------------

import numpy as np

#------------------ User specification --------------------
pdb_name = 'protien_name'  # CHARMM pdb format w/o file extension
mode_id = 10
N_FRAME = 20
N_AMP   = 2

vec_name = 'mode%d_eigenvectors_protein_name-state_name.dat'%mode_id
# vec_name is the file containing eigenvectors of a certain mode.
# It has the following format:
# {x1} {y1} {z1}
# {x2} {y2} {z2}
# ...
# {xn} {yn} {zn}

#---------- CHARMM PDB format ----------
# entry name        # colunm number
header		   = [] #0
atom_serial	   = [] #1
atom_name	   = [] #2
residue_name   = [] #3
residue_serial = [] #4
x_coor         = [] #5
y_coor         = [] #6
z_coor         = [] #7
occupancy      = [] #8
b_factor       = [] #9
chain_id       = [] #10

#---------- Eigenvector ----------
vec_x = []
vec_y = []
vec_z = []

#---------- Reading data ----------
print "Reading eigenvector arrays ...\n"
vec_src = np.genfromtxt(vec_name)
vec_x = vec_src[:,0]
vec_y = vec_src[:,1]
vec_z = vec_src[:,2]

print "Reading PDB file ... \n"
with open(pdb_name+'.pdb','r') as pdb_file:
    atom_count = 0
    for each_line in pdb_file:
        if each_line.startswith('ATOM'):
            atom_count += 1
            header.append(each_line[0:6])
            atom_serial.append(each_line[6:11])
            atom_name.append(each_line[11:17])
            residue_name.append(each_line[17:21])
            residue_serial.append(each_line[21:30])
            x_coor.append(float(each_line[30:38]))
            y_coor.append(float(each_line[38:46]))
            z_coor.append(float(each_line[46:54]))
            occupancy.append(each_line[54:60])
            b_factor.append(each_line[60:66])
            chain_id.append(each_line[66:76])
			
print "%d atom entries was recorded.\n"%atom_count

#---------- Generating output file ----------
out_prefix = 'nma-movie-'
out_name   = out_prefix + pdb_name + '-mode%d'%mode_id + '.pdb'
print "Generating normal mode movie file: %s...\n"%out_name

out_file = open(out_name,'w')
print "Generating normal mode movies ... \n"
# Moving forward along the eigenvector ...
for i in range(0, N_FRAME):
    new_x = []
    new_y = []
    new_z = []
    res_count = -1  # count the number of residues
    tmp_resid = '' # temparorily store residue id
    for j in range(0, atom_count):
        if (residue_serial[j] == tmp_resid):
            new_x.append(x_coor[j] + i*N_AMP*float(vec_x[res_count]))
            new_y.append(y_coor[j] + i*N_AMP*float(vec_y[res_count]))
            new_z.append(z_coor[j] + i*N_AMP*float(vec_z[res_count]))
        else:
            tmp_resid = residue_serial[j]
            res_count += 1
            #print res_count
            new_x.append(x_coor[j] + i*N_AMP*float(vec_x[res_count]))
            new_y.append(y_coor[j] + i*N_AMP*float(vec_y[res_count]))
            new_z.append(z_coor[j] + i*N_AMP*float(vec_z[res_count]))
        out_file.write("%s%s%s%s%s%8.3f%8.3f%8.3f%s%s%s\n" % 
            (header[j],atom_serial[j],atom_name[j],residue_name[j],residue_serial[j],new_x[j],new_y[j],new_z[j],occupancy[j],b_factor[j],chain_id[j]))
    out_file.write('END\n')
# Moving backward along the eigenvector ...
for i in list(reversed(range(0, N_FRAME))):
    new_x = []
    new_y = []
    new_z = []
    res_count = -1  # count the number of residues
    tmp_resid = ''  # temparorily store residue id
    for j in range(0, atom_count):
        if (residue_serial[j] == tmp_resid):
            new_x.append(x_coor[j] + i*N_AMP*float(vec_x[res_count]))
            new_y.append(y_coor[j] + i*N_AMP*float(vec_y[res_count]))
            new_z.append(z_coor[j] + i*N_AMP*float(vec_z[res_count]))
        else:
            tmp_resid = residue_serial[j]
            res_count += 1
            new_x.append(x_coor[j] + i*N_AMP*float(vec_x[res_count]))
            new_y.append(y_coor[j] + i*N_AMP*float(vec_y[res_count]))
            new_z.append(z_coor[j] + i*N_AMP*float(vec_z[res_count]))
        out_file.write("%s%s%s%s%s%8.3f%8.3f%8.3f%s%s%s\n" % 
            (header[j],atom_serial[j],atom_name[j],residue_name[j],residue_serial[j],new_x[j],new_y[j],new_z[j],occupancy[j],b_factor[j],chain_id[j]))
    out_file.write('END\n')
print "Done.\n"

out_file.close()