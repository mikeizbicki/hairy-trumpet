#!/bin/sh

set -e

for file in raw/wiki__page=*; do
    echo "$file"
    python3 scripts/apply_masks.py "$file" domains/election2024
    python3 scripts/apply_masks.py "$file" domains/election2024 --dpsize=sentence
done

for domain in domains/*; do
    for file in raw/*pages_file="$(basename "$domain")"*; do
        echo $file
        python3 scripts/apply_masks.py "$file" "$domain" --dpsize=sentence
        python3 scripts/apply_masks.py "$file" "$domain" --dpsize=paragraph
    done
done
