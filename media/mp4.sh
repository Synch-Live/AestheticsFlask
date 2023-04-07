#!/bin/zsh

indir="2-img"
outdir="web/static/videos"

if [ ! -d "$indir" ]; then
    echo "Script expects a directory called $indir to pull simulations from"
    exit
fi

if [ ! -d "$outdir" ]; then
    mkdir -p -v $outdir
fi


for dir in $indir/*; do
    [ -d "$dir" ] || continue

    name=$(basename $dir)
    echo "Creating vid from $dir to $outdir/$name.vid"

    if [[ -e "$dir/0.jpg" ]]; then
        ffmpeg -framerate 12 -i $dir/%d.jpg -r 24 -s 800x600 $outdir/$name.mp4
    else
        ffmpeg -framerate 12 -pattern_type glob -i "$dir"'/*.jpg' -r 24 -s 800x600 $outdir/$name.mp4
    fi

done

