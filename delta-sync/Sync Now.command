#!/bin/bash
# Saves your current Delta balance to today's row in the tracker right now.
cd "$(dirname "$0")" || exit 1
/usr/bin/python3 delta_sync.py "$@"
read -r -p "Press Return to close." _
