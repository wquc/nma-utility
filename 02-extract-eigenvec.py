#---------------------------------------------------------
# Get eigenvectors of certain modes from file (source.dat)
# containing eigenvectors of all modes, source.dat has the 
# following format:
# {mode_id} {eigen_value}: {x1} {y1} {z1} ... {xn} {yn} {zn}
#
#                                                     Q.W.
#---------------------------------------------------------

import numpy as np

# Do not add filename extension here.
inp_name = "source"

def extract_eigenvec(mode):
    # step 1. Read from data
    print "reading data ..."
    with open(inp_name + ".dat", 'r') as inp_file:
        line_count = 0
        while (line_count < mode):
            new_line = inp_file.readline().strip().replace(":"," ")
            line_count = line_count + 1
        tmp_list = new_line.split(" ")
        new_list = [item for item in filter(None, new_line.split(' '))]
        eigen_mode  = new_list[0]
        eigen_value = new_list[1]
        eigen_vec = np.delete(np.array(new_list), [0,1])
        print "eigen_mode is: ",  eigen_mode
        print "eigen_value is: ", eigen_value
        print "length of eigenvector is: ", len(eigen_vec)/3

        len_of_vec = len(eigen_vec)/3

    # step 2. Write data into file
    out_name =  "mode" + str(mode) + "_" + inp_name
    print out_name
    with open(out_name + ".dat", 'w') as out_file:
        for i in range(0, len_of_vec):
            out_file.write('%s\t%s\t%s\n'%(eigen_vec[i*3+0], eigen_vec[i*3+1], eigen_vec[i*3+2]))

# usage:
if __name__=="__main__":
    extract_eigenvec(7)