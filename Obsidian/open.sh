#!/bin/bash
set -e

source /home/user/Documents/encryption/venv/bin/activate
cd /home/user/Documents/Obsidian
python /home/user/Documents/encryption/encryption.py --action decrypt /home/user/Documents/Obsidian
echo "Obsidian archive opened successfully"
