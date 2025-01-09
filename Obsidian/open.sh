#!/bin/bash
set -e

source /path/to/venv/venv/bin/activate
cd /path/to/Obsidian/dir
python /path/to/tc-obsidian.py --action decrypt /path/to/Obsidian/dir
echo "Obsidian archive opened successfully"
