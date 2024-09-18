#!/bin/sh

set -e

for file in raw/wiki__page=*; do
    echo "$file"
    python3 scripts/apply_masks.py "$file" masks/election2024
    python3 scripts/apply_masks.py "$file" masks/election2024 --dpsize=sentence
done

for mask in masks/*; do
    for file in raw/*pages_file="$(basename "$mask")"*; do
        echo $file
        python3 scripts/apply_masks.py "$file" "$mask" --dpsize=sentence
        python3 scripts/apply_masks.py "$file" "$mask" --dpsize=paragraph
    done
done
