# Source this script from VMD TkConsole to generate GIFs from MD trajectory.

proc make_animated_gif {} {
    set nframes [molinfo top get numframes]
    for { set iframe 0 } { $iframe < $nframes } { incr iframe 1} {
        animate goto $iframe
        set filename snap.[format "%04d" $iframe].rgb
        render snapshot $filename
    }
    puts "Converting tmp files to gif ... \n"
    exec convert -delay 10 -loop 0 snap.*.rgb movie.gif
    puts "Deleting tmp files ... \n"
    exec /bin/sh -c "rm snap.*.rgb"
    puts "Done. \n"
}