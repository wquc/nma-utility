# Generate segments from PDB file.
# This script will generate pdb files for each subunit of a tetradecamer(14mer).
# It assumes the input pdb file only contains lines starts with 'ATOM  '.
# Author: Qi Wang (wang2qi@mail.uc.edu)

from string import ascii_uppercase

def gen_seg(segid, pdbname, segname):
	print "Generating segments for segment: %s"%segid
	outfile = open(segname, 'w')
	with open(pdbname, 'r') as pdbfile:
		for eachline in pdbfile:
			if(segid==eachline[20:22].strip()):
				outfile.write(eachline)
	outfile.close()

pdbname="pdb_name.pdb"
namepref="seg-"
segset = ascii_uppercase[0:14]

for segid in segset:
	segname=namepref + segid.lower() + '.pdb'
	gen_seg(segid, pdbname, segname)


