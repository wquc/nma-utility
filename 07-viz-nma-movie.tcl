# This function was written initially to load vmd-movie.pdb files
# of different modes to visualize their motions.
# It essentially just load and set the representation of a pdb structure.
# Author: Qi Wang(wang2qi@mail.uc.edu)

proc wq_show_movie {} {
	set molid [ molinfo list ]
	puts $molid
	mol delete $molid
	puts "Enter the .pdb file to be read:"
	flush stdout
	set filename [gets stdin]

	display resize 800 800
	display projection Orthographic
	display depthcue off

	mol addfile $filename
	mol representation Tube 0.6 12
	mol color Segname
	set molid [ molinfo list ]
	mol addrep $molid
	mol delrep 0 $molid
}
