proc choice {elements} {
    set l [llength $elements]
    set c [expr int(rand()*$l)]
    return [lindex $elements $c]
}

proc hidden_char word {
    set l [expr int([string length $word]/2)-1]
    for {set i 0} {$i <= $l} {incr i} {
        set a [expr int(rand()*$l)]
        set word [string replace $word $a $a *]
    }
    return $word
}

proc clean {} {
    global lose_level word char_input indice_word
    set lose_level 0
    set word ""
    set indice_word ""
    set char_input [lindex [split $char_input \n] 0]\n
    .drawing delete player
}

proc play {} {
    global indice_word title_text list_word word
    clean
    set word [choice $list_word]
    set title_text [format $title_text [expr [string length $word]-1]]
    set indice_word [hidden_char $word]
}

proc write key {
    global word score lose_level char_input indice_word
    set lword [split $word ""]
    set ikey [lsearch $lword $key]
    if {[string length $key] > 1} {
        return 0
    }
    if {$ikey != -1} {
        set tiw [lreplace [split $indice_word ""] $ikey $ikey $key]
        set indice_word ""
        foreach char $tiw {
            set indice_word $indice_word$char
        }
        if {$indice_word == $word} {
            tk_messageBox -message "You are found the word"
            play
        }
    } else {
        set char_input "$char_input$key "
        incr lose_level
        lose $lose_level
    }
}
proc lose level {
    switch $level {
        1 {.drawing create oval 50 50 100 100 -width 10 -tag player}
        2 {.drawing create line 75 100 75 200 -width 10 -tag player}
        3 {.drawing create line 75 200 100 250 -width 10 -tag player}
        4 {.drawing create line 75 200 50 250 -width 10 -tag player}
        default {
            .drawing itemconfigure player -fill red
            global word
            tk_messageBox -message "You are losed, it was $word"
            play
        }
    }
}