#!/bin/bash

# run python script
python3 domain_checker.py

# Check if the domains.txt has at least 1000 lines
lines=$(wc -l < domains.txt)
if [ $lines -lt 1000 ]; then
    echo "domains.txt does not have at least 1000 rows. Exiting..."
    exit 1
fi

# Git commit and push
timestamp=$(date)
#cd /path/to/your/repository

# Set GIT credentials (replace with your own)
export GIT_USERNAME="username"
export GIT_TOKEN="personal-access-token"

# Commit changes
git add domains.txt
git commit -m "[$timestamp] - MX validated and updated domains"

# Set remote URL with access token
git remote set-url origin https://$GIT_USERNAME:$GIT_TOKEN@github.com/$GIT_USERNAME/repository.git

# Push to GitHub
git push origin master

echo "Updated domains.txt committed and pushed to repository."
