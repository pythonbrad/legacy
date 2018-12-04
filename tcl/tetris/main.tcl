set w 320
set h 640

set block_size 20

set v 20

set b1 "{0 0 $block_size $block_size} {$block_size 0 [expr {2 * $block_size}] $block_size} {[expr {2 * $block_size}] 0 [expr {3 * $block_size}] $block_size} {[expr {3 * $block_size}] 0 [expr {4 * $block_size}] $block_size}"

set b2 "{0 0 $block_size $block_size} {$block_size 0 [expr {2 * $block_size}] $block_size} {0 $block_size $block_size [expr {2 * $block_size}]} {$block_size $block_size [expr {2 * $block_size}] [expr {2 * $block_size}]}"

set b3 "{0 0 $block_size $block_size} {$block_size 0 [expr {2 * $block_size}] $block_size} {[expr {2 * $block_size}] 0 [expr {3 * $block_size}] $block_size} {$block_size $block_size [expr {2 * $block_size}] [expr {2 * $block_size}]}"

set b4 "{0 0 $block_size $block_size} {$block_size 0 [expr {2 * $block_size}] $block_size} {[expr {2 * $block_size}] 0 [expr {3 * $block_size}] $block_size} {0 $block_size $block_size [expr {2 * $block_size}]}"

set b5 "{0 0 $block_size $block_size} {$block_size 0 [expr {2 * $block_size}] $block_size} {[expr {2 * $block_size}] 0 [expr {3 * $block_size}] $block_size} {[expr {2 * $block_size}] $block_size [expr {3 * $block_size}] [expr {2 * $block_size}]}"

set b6 "{0 0 $block_size $block_size} {$block_size 0 [expr {2 * $block_size}] $block_size} {$block_size $block_size [expr {2 * $block_size}] [expr {2 * $block_size}]} {[expr {2 * $block_size}] $block_size [expr {3 * $block_size}] [expr {2 * $block_size}]}"

set b7 "{$block_size 0 [expr {2 * $block_size}] $block_size} {[expr {2 * $block_size}] 0 [expr {3 * $block_size}] $block_size} {0 $block_size $block_size [expr {2 * $block_size}]} {$block_size $block_size [expr {2 * $block_size}] [expr {2 * $block_size}]}"

set rb1 "{0 0 $block_size $block_size} {0 $block_size $block_size [expr {2 * $block_size}]} {0 [expr {2 * $block_size}] $block_size [expr {3 * $block_size}]} {0 [expr {3 * $block_size}] $block_size [expr {4 * $block_size}]}"

set rb3a "{$block_size 0 [expr {2 * $block_size}] $block_size} {0 $block_size $block_size [expr {2 * $block_size}]} {$block_size $block_size [expr {2 * $block_size}] [expr {2 * $block_size}]} {$block_size [expr {2 * $block_size}] [expr {2 * $block_size}] [expr {3 * $block_size}]}"

set rb3b "{0 0 $block_size $block_size} {0 $block_size $block_size [expr {2 * $block_size}]} {0 [expr {2 * $block_size}] $block_size [expr {3 * $block_size}]} {$block_size $block_size [expr {2 * $block_size}] [expr {2 * $block_size}]}"

set rb4 "{0 0 $block_size $block_size} {$block_size 0 [expr {2 * $block_size}] $block_size} {$block_size $block_size [expr {2 * $block_size}] [expr {2 * $block_size}]} {$block_size [expr {2 * $block_size}] [expr {2 * $block_size}] [expr {3 * $block_size}]}"

set rb5 "{0 0 $block_size $block_size} {$block_size 0 [expr {2 * $block_size}] $block_size} {0 $block_size $block_size [expr {2 * $block_size}]} {0 [expr {2 * $block_size}] $block_size [expr {3 * $block_size}]}"

set rb6 "{$block_size 0 [expr {2 * $block_size}] $block_size} {0 $block_size $block_size [expr {2 * $block_size}]} {$block_size $block_size [expr {2 * $block_size}] [expr {2 * $block_size}]} {0 [expr {2 * $block_size}] $block_size [expr {3 * $block_size}]}"

set rb7 "{0 0 $block_size $block_size} {0 $block_size $block_size [expr {2 * $block_size}]} {$block_size $block_size [expr {2 * $block_size}] [expr {2 * $block_size}]} {$block_size [expr {2 * $block_size}] [expr {2 * $block_size}] [expr {3 * $block_size}]}"

set current_block ""
set current_block_name ""
set high_y_block 50

set list_block [list $b1 $b2 $b3 $b4 $b5 $b6 $b7 $rb1 $rb3a $rb3b $rb4 $rb5 $rb6 $rb7]
set list_block_color [list cyan yellow violet orange blue red green cyan violet violet orange blue red green]

set score "Score: 0"

proc add_score {} {
    global score
    set i [lindex $score 1]
    incr i
    set score "Score: $i"
}

proc random {x} {
    return [expr {int(rand() * $x)}]
}

proc delete_line {} {
    global block_size
    global w h
    for {set i $h} {$i > 0} {incr i -1} {
        set blocks_delete [.canevas find overlapping 0 $i $w $i]
        if {[llength $blocks_delete]-5 > $w/$block_size} {
            foreach block_delete $blocks_delete {
                add_score
                .canevas delete $block_delete
            }
        }
    }
}

proc create {coords color} {
    global current_block current_block_name
    foreach coord $coords {
        lappend current_block_name [.canevas create rectangle $coord -fill $color]
    }
    set current_block $coords
    add_score
}

proc is_collision {} {
    global current_block current_block_name
    foreach block_coords $current_block {
        set x1 [lindex $block_coords 0]
        set y1 [lindex $block_coords 1]
        set x2 [lindex $block_coords 2]
        set y2 [lindex $block_coords 3]
        set x1 [expr {$x1 + 1}]
        set x2 [expr {$x2 - 1}]
        set objs [.canevas find overlapping $x1 $y1 $x2 $y2]
        foreach obj $objs {
            if {[lsearch $current_block_name $obj] == -1} {
                return True
            }
        }
    }
    return False
}

proc b_move {direction vitesse} {
    global current_block current_block_name high_y_block
    global w h v
    set new_coords ""
    set moving True
    foreach block_coords $current_block {
        set x1 [lindex $block_coords 0]
        set y1 [lindex $block_coords 1]
        set x2 [lindex $block_coords 2]
        set y2 [lindex $block_coords 3]
        if {$direction == "y"} {
            set y1 [expr {$y1 + $vitesse}]
            set y2 [expr {$y2 + $vitesse}]
        } elseif {$direction == "x"} {
            set x1 [expr {$x1 + $vitesse}]
            set x2 [expr {$x2 + $vitesse}]
        }
        if {$x1 < 0 || $x2 > $w} {
            set moving False
            break
        } elseif {$y2 > $h || [is_collision]} {
            set moving False
            set high_y_block $y1
            set current_block_name ""
            break
        } else {
            set new_coord [list $x1 $y1 $x2 $y2]
            lappend new_coords $new_coord
        }
    }
    if $moving {
        set current_block $new_coords
        set i 0
        foreach block_name $current_block_name {
            .canevas coords $block_name [lindex $current_block $i]
            incr i
        }
    }
}

proc anim {} {
    global b1 b2 b3 b4 b5 b6 b7
    global current_block_name list_block list_block_color v
    global high_y_block block_size score
    if {$current_block_name == ""} {
        set i [random [llength $list_block]]
        create [lindex $list_block $i] [lindex $list_block_color $i]
    } else {b_move y $v}
    if {$high_y_block > $block_size} {
        delete_line
        after 500 anim
    } else {tk_messageBox -title Finish -message $score}
}
label .label_score -textvariable score -font 10
pack .label_score
canvas .canevas -width $w -height $h
pack .canevas
bind . <Right> {b_move x $v}
bind . <Left> {b_move x -$v}
bind . <Down> {b_move y $v}

anim
