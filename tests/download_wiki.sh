#!/bin/sh

set -e

for file in domains/*; do
    echo $file
    python3 scripts/download_wiki.py --pages_file="$file"
done

pages='
2024_United_States_presidential_election
2024_United_States_elections
Kamala_Harris_2024_presidential_campaign
Donald_Trump_2024_presidential_campaign
'

for page in $pages; do
    echo $page
    python3 scripts/download_wiki.py --page="$page"
    python3 scripts/download_wiki.py --page="$page" --recursive_depth=1
done
