#------------------------------------------------------------------------
# Load vmd-movie.pdb files containing different frames of a NMA mode.
#------------------------------------------------------------------------

proc show_movie {} {
    set molid [ molinfo list ]
    puts $molid
    mol delete $molid
    puts "Enter the PDB file to be read:"
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