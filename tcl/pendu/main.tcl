source vars.tcl
source procs.tcl

#gui
wm title . $title
wm iconphoto . $icon

#INFORMATION
pack [frame .information] -side left
pack [frame .title] -side top -in .information
pack [label .title.text -textvariable title_text]
pack [label .title.indice_word -textvariable indice_word]

pack [frame .body] -pady 30 -in .information
pack [label .body.score -text {SCORE: }] -side left
pack [label .body.score_nb -textvariable score] -side left

pack [frame .footer] -in .information
pack [label .footer.message -textvariable char_input]

#DRAWING
pack [canvas .drawing -background grey -width 150]
.drawing create line 10 10 10 300 -tag pend
.drawing create line 10 10 150 10 -tag pend
.drawing create line 75 10 75 50 -tag pend

#BINDING
bind . <Key> {write %K}

#START
play