#!/bin/zsh

USERDIR="/Users/$(whoami)"
APPSUPPORTDIR="$USERDIR/Library/Application Support/Anki2"
COLLDIR="$APPSUPPORTDIR/User 1"
MEDIARDIR="$COLLDIR/collection.media"

# locate the file we downloaded
FILE="$(ls $HOME/Documents/mp3 | head -1)"
# play it so we can hear
afplay "$HOME/Documents/mp3/$FILE"
# copy it to the collection.media directory
cp $HOME/Documents/mp3/$FILE "$MEDIARDIR/$FILE"
# insert the link in the Anki field
echo "[sound:$FILE]"