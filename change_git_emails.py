#! /usr/bin/env python3

import argparse
import os
import subprocess
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Replace all Git commit emails in a repo.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--old-email', required=True,
                        help="Old email address to replace.")
    parser.add_argument('-n', '--new-email', required=False,
                        default="65621+sujeevraja@users.noreply.github.com",
                        help="New email address to use.")
    parser.add_argument('-r', '--repo-path', required=True,
                        help="Path to the target Git repository.")
    return parser.parse_args()

def verify_git_repo(repo_path):
    if not os.path.isdir(repo_path):
        sys.exit(f"Error: '{repo_path}' is not a valid directory.")
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        sys.exit(f"Error: '{repo_path}' is not a Git repository.")

def rewrite_git_history(repo_path, old_email, new_email):
    script = f"""
    git filter-branch --env-filter '
    if [ "$GIT_COMMITTER_EMAIL" = "{old_email}" ]
    then
        export GIT_COMMITTER_EMAIL="{new_email}"
    fi
    if [ "$GIT_AUTHOR_EMAIL" = "{old_email}" ]
    then
        export GIT_AUTHOR_EMAIL="{new_email}"
    fi
    ' --tag-name-filter cat -- --branches --tags
    """
    try:
        subprocess.run(script, cwd=repo_path, shell=True, check=True, executable='/bin/bash')
        print("Git history successfully rewritten.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error while rewriting Git history: {e}")

def main():
    args = parse_args()
    verify_git_repo(args.repo_path)
    rewrite_git_history(args.repo_path, args.old_email, args.new_email)

if __name__ == '__main__':
    main()
