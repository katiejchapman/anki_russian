cd ~/Library/Application\ Support/Anki2/User\ 1/collection.media/
for i in *.mp3; do
    if (($(file "$i" | grep -wic Ogg))); then
        mv "$i" "${i%.*}.ogg" 
    fi
done

for i in *.ogg; 
    do if [ ! -f "${i%.*}.mp3" ]; then
        ffmpeg -i "$i" "${i%.*}.mp3" 
    fi;
done