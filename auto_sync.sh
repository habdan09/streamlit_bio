#!/bin/bash
while true; do
    # Check for changes
    if [ -n "$(git status --porcelain)" ]; then
        git add .
        git commit -m "Auto-sync: $(date)"
        git push
        echo "Changes pushed at $(date)"
    fi
    sleep 10  # Check every 10 seconds
done
