#vars
set text_score1 "Score player1:0"
set text_score2 "Score player2:0"
set speed 10
set alpha 60
set dx [expr cos($alpha)]
set dy [expr sin($alpha)]
set sens 1
set cw 300
set ch 300

#procs
proc move {item d} {
    global speed ch cw
    set coords [.drawing coords $item]
    set x1 [lindex $coords 0]
    set y1 [expr [lindex $coords 1]+[expr $speed*$d]]
    set x2 [lindex $coords 2]
    set y2 [expr [lindex $coords 3]+[expr $speed*$d]]
    if {$y1-$speed < 0 || $y2+$speed > $ch} {
        return 0
    }
    .drawing coords $item $x1 $y1 $x2 $y2
}

proc robot item {
    set coords [.drawing coords $item]
    set x1 [lindex $coords 0]
    set y1 [lindex $coords 1]
    set x2 [lindex $coords 2]
    set y2 [lindex $coords 3]
    set size [expr $y2-$y1]
    set coords [.drawing coords ball]
    set y1 [lindex $coords 1]
    set y2 [expr $y1+$size]
    .drawing coords $item $x1 $y1 $x2 $y2
}

proc collision item {
    global speed
    set coords [.drawing coords $item]
    set x1 [expr [lindex $coords 0]-$speed]
    set y1 [expr [lindex $coords 1]-$speed]
    set x2 [expr [lindex $coords 2]+$speed]
    set y2 [expr [lindex $coords 3]+$speed]
    set obj_coll [.drawing find overlapping $x1 $y1 $x2 $y2]
    if {[llength $obj_coll] > 1} {
        return 1
    } else {
        return 0
    }
}

proc anim {} {
    global speed dx dy sens ch cw ia1 ia2 text_score1 text_score2

    set coords [.drawing coords ball]
    set x1 [expr [lindex $coords 0]+$dx*$speed*$sens]
    set y1 [expr [lindex $coords 1]+$dy*$speed*$sens]
    set x2 [expr [lindex $coords 2]+$dx*$speed*$sens]
    set y2 [expr [lindex $coords 3]+$dy*$speed*$sens]
    .drawing coords ball $x1 $y1 $x2 $y2
    if [collision ball] {
        set dx -$dx
    }
    if {$y1-$speed < 0 || $y2+$speed > $ch} {
        set dy -$dy
    }
    if {$x1-$speed < 0} {

        set score [lindex [split $text_score1 :] 1]
        set text_score1 "[lindex [split $text_score1 :] 0]:[expr $score+1]"
        set dx -$dx
    }
    if {$x2+$speed > $cw} {
        set score [lindex [split $text_score2 :] 1]
        set text_score2 "[lindex [split $text_score2 :] 0]:[expr $score+1]"
        set dx -$dx
    }
    if $ia1 {robot player1}
    if $ia2 {robot player2}
    after 50 anim
}

#GUI
pack [frame .information] -side left

pack [frame .head] -side top -in .information
pack [label .head.score1 -textvariable text_score1]
pack [label .head.score2 -textvariable text_score2]
pack [label .head.iaLabel1 -text IA1]
pack [checkbutton .head.ia1 -variable ia1]
pack [label .head.iaLabel2 -text IA2]
pack [checkbutton .head.ia2 -variable ia2]

pack [canvas .drawing -background grey -width $cw -height $ch] -side right

.drawing create oval 100 100 125 125 -fill orange -outline orange -tag ball
.drawing create rectangle 10 10 20 70 -fill red -outline red -tag player1
.drawing create rectangle 280 10 290 70 -fill blue -outline blue -tag player2

#binding
bind . <Up> {move player1 -1}
bind . <Down> {move player1 1}
bind . <w> {move player2 -1}
bind . <s> {move player2 1}

#animation
after 50 anim
