#!/bin/bash

# Setup environment
source /home/emailabuseverify/virtualenv/disposable-email-domain-list/3.8/bin/activate && cd /home/emailabuseverify/disposable-email-domain-list
# pip install -r requirements.txt

# run python script
python3 main.py

# # Check if the domains.txt has at least 1000 lines
lines=$(wc -l < domains.txt)
if [ $lines -lt 1000 ]; then
    echo "domains.txt does not have at least 1000 rows. Exiting..."
    exit 1
fi

# Git commit and push
timestamp=$(date)
#cd /path/to/your/repository

# Set GIT credentials (replace with your own)
git config --global user.name "Auto Updater"
git config --global user.email ""

export GIT_USERNAME=""
export GIT_TOKEN="" # your personal access token

git fetch https://$GIT_USERNAME:$GIT_TOKEN@github.com/groundcat/disposable-email-domain-list.git

# Commit changes
git add domains.txt
git add domains.json
git commit -m "[$timestamp] - MX validated and updated domains"

# Set remote URL with access token
git remote set-url origin https://$GIT_USERNAME:$GIT_TOKEN@github.com/groundcat/disposable-email-domain-list.git

# Push to GitHub
git push origin master

echo "Updated domains.txt committed and pushed to repository."
