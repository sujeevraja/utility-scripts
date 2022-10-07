#!/bin/sh

# Script source:
# https://help.github.com/en/github/using-git/changing-author-info
#
# To run this script, update values of OLD_EMAIL, CORRECT_NAME and
# CORRECT_EMAIL. Then, run the script in the git repo to be updated.
# Update remote with `git push --force --tags origin 'refs/heads/*'`.

git filter-branch -f --env-filter '

OLD_EMAIL="sujeevraja26@gmail.com"
CORRECT_NAME="Sujeevraja Sanjeevi"
CORRECT_EMAIL="sujeevraja.sanjeevi@smartnomad.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
