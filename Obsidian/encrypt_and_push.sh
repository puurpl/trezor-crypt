#!/bin/bash
set -e

source /path/for/venv/venv/bin/activate
cd /path/for/Obsidian/dir
python /path/for/tc-obsidian.py --action encrypt /path/for/Obsidian/dir
git add /path/for/Obsidian/dir/*
git ls-files --deleted -z | xargs -0 git rm
git commit -m "Script commit"
git push -u origin main
read -p "Are you sure you want to proceed with decryption? (y/n): " confirm
if [[ $confirm != [yY] ]]; then
    echo "Decryption aborted."
    exit 0
fi

python /path/for/tc-obsidian.py --action decrypt /path/for/Obsidian/dir
