#!/bin/sh

for f in raw/*; do
    for names in names/*; do
        echo "$f $names"
        python3 scripts/hairy_trumpet.py "$f" --names=$names
    done
done
