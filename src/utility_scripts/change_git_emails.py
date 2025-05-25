#! /usr/bin/env python3

import argparse
import os
import subprocess
import sys
import shutil

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
    
    # Check if git-filter-repo is installed
    if not shutil.which('git-filter-repo'):
        sys.exit("Error: git-filter-repo is not installed. Please install it first:\n"
                "pip3 install git-filter-repo")

def rewrite_git_history(repo_path, old_email, new_email):
    try:
        # Create a backup of the repository
        backup_path = f"{repo_path}_backup"
        if os.path.exists(backup_path):
            sys.exit(f"Error: Backup directory '{backup_path}' already exists. Please remove it first.")
        
        print(f"Creating backup at {backup_path}...")
        shutil.copytree(repo_path, backup_path)
        
        # Run git-filter-repo to rewrite the history
        cmd = [
            'git-filter-repo',
            '--email-callback',
            f'return email.replace("{old_email}", "{new_email}")',
            '--force'
        ]
        
        subprocess.run(cmd, cwd=repo_path, check=True)
        print("Git history successfully rewritten.")
        print(f"Original repository backed up at: {backup_path}")
        
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error while rewriting Git history: {e}")
    except Exception as e:
        sys.exit(f"Error: {e}")

def main():
    args = parse_args()
    verify_git_repo(args.repo_path)
    rewrite_git_history(args.repo_path, args.old_email, args.new_email)

if __name__ == '__main__':
    main()
