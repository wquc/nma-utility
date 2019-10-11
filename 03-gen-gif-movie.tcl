# Source this script from VMD TkConsole to generate GIFs from MD trajectory.
# Parameters:
#  moviename - output name (without the .gif extension) for the GIF file
#  frameskip - number of frames to be skipped (default is 1)
proc makemovie { moviename { frameskip 1}} {
    set nframes [molinfo top get numframes]
    for { set iframe 0 } { $iframe < $nframes } { incr iframe $frameskip} {
        animate goto $iframe
        set filename tmp.[format "%05d" [expr $iframe+1]].ppm
        render TachyonLOptiXInternal $filename
    }
    puts "Converting tmp files to gif ... \n"
    exec convert -delay 15 -loop 0 tmp.*.ppm $moviename.gif
    puts "Deleting tmp files ... \n"
    exec /bin/sh -c "rm tmp.*.ppm"
    puts "Done. \n"
}