# Source this script from VMD TkConsole to generate GIFs from MD trajectory.

proc make_animated_gif {} {
	set sel [atomselect 0 "all"]
	set n [molinfo top get numframes]
	for { set i 0 } { $i < $n } { incr i 100} {
	animate goto $i
	set filename snap.[format "%04d" $i].rgb
	render snapshot $filename
	}
	puts "Converting tmp files to gif ... \n"
	exec convert -delay 10 -loop 0 snap.*.rgb movie.gif
	puts "Deleting tmp files ... \n"
	exec /bin/sh -c "rm snap.*.rgb"
	puts "Done. \n"
} 
