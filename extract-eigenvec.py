import numpy as np

''' get eigenvectors of certain modes from file (source.dat) containing eigenvectors of all modes
	source.dat has the following format:
	{mode_id} {eigen_value}: {x1} {y1} {z1} {x2} {y2} {z2} ... {xn} {yn} {zn}
'''

dbspace = "  "
udscore = "_"
extsn = ".dat"

inp_name = "source"

def extract_eigenvec(mode):
	# step 1. Read from data
	print "reading data ..."
	with open(inp_name + extsn, 'r') as inp_file:
		line_count = 0
		while (line_count < mode):
			new_line = inp_file.readline().strip().replace(":"," ")
			line_count = line_count + 1
		new_list = new_line.split(dbspace)
		eigen_mode = new_list[0]
		eigen_value = new_list[1]
		eigen_vec = np.delete(np.array(new_list), [0,1])
		print "eigen_mode is: ", eigen_mode
		print "eigen_value is: ", eigen_value
		print "length of eigenvector is: ", len(eigen_vec)/3

		len_of_vec = len(eigen_vec)/3

	# step 2. Write data into file
	out_name =  "mode" + str(mode) + udscore + inp_name
	print out_name
	with open(out_name + extsn, 'w') as out_file:
		for i in range(0, len_of_vec):
			out_file.write('%s\t%s\t%s\n'%(eigen_vec[i*3+0], eigen_vec[i*3+1], eigen_vec[i*3+2]))

# usage:
extract_eigenvec(7)
