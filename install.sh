#!/bin/bash

SRCPATH="$HOME/Dropbox/Dev/math/kate-greek-snippets"

mkcd(){
    mkdir -p "$1"
    cd "$1"
}

mkcd "$HOME/.config/autokey/data/My Phrases/math-gen" && {

# later improve: not delete folder file
rm * .??*

python3 "$SRCPATH/gen_autokey.py" < "$SRCPATH/list.md"

}
