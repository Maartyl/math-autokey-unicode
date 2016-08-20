#!/bin/bash

SRCPATH="$HOME/Dropbox/Dev/math/autokey-unicode-abbreviations"

mkcd(){
    mkdir -p "$1"
    cd "$1"
}

mkcd "$HOME/.config/autokey/data/math-gen" && {

    # later improve: not delete folder file
    rm * .??* || true

    python3 "$SRCPATH/gen_autokey.py" < "$SRCPATH/list.md" && {
        
        killall autokey
        (autokey &)  # start in background

    }

}


