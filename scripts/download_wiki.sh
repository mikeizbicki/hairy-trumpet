#!/bin/sh

#python3 scripts/download_wiki.py --page=2024_United_States_presidential_election --recursive_depth=0
#python3 scripts/download_wiki.py --page=2024_United_States_presidential_election --recursive_depth=1
python3 scripts/download_wiki.py --page=2024_United_States_elections --recursive_depth=0
python3 scripts/download_wiki.py --page=2024_United_States_elections --recursive_depth=1
