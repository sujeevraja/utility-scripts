#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(cmd)}")
        print(f"Error message: {e.stderr}")
        sys.exit(1)

def is_git_repo(path):
    """Check if the given path is a git repository."""
    try:
        subprocess.run(['git', '-C', path, 'rev-parse', '--is-inside-work-tree'],
                      check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def has_uncommitted_changes(path):
    """Check if there are uncommitted changes in the repository."""
    try:
        subprocess.run(['git', '-C', path, 'diff-index', '--quiet', 'HEAD', '--'],
                      check=True, capture_output=True)
        return False
    except subprocess.CalledProcessError:
        return True

def main():
    parser = argparse.ArgumentParser(
        description='Remove a file from Git history across all branches',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sensitive/password.txt                    # Remove file from current directory repo
  %(prog)s -r /path/to/repo sensitive/password.txt  # Remove file from specified repo
  %(prog)s --repo /path/to/repo config.json         # Remove file from specified repo

Note: The file path should be relative to the repository root
Note: This script requires git-filter-repo to be installed
      Install with: pip3 install git-filter-repo
        """
    )
    parser.add_argument('-r', '--repo', default='.',
                      help='Path to the Git repository (default: current directory)')
    parser.add_argument('file_path', help='Path to the file to remove from history')
    args = parser.parse_args()

    # Check if git-filter-repo is installed
    try:
        subprocess.run(['git-filter-repo', '--version'],
                      check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: git-filter-repo is not installed")
        print("Please install it with: pip3 install git-filter-repo")
        sys.exit(1)

    repo_path = Path(args.repo).resolve()
    file_to_remove = args.file_path

    # Check if repository path exists
    if not repo_path.is_dir():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)

    # Check if we're in a git repository
    if not is_git_repo(repo_path):
        print(f"Error: Not in a Git repository: {repo_path}")
        sys.exit(1)

    # Check if the file exists in the current state
    file_path = repo_path / file_to_remove
    if not file_path.is_file():
        print(f"Warning: File '{file_to_remove}' does not exist in the current state.")
        print("This is okay if you want to remove it from history even if it's not present now.")
        response = input("Do you want to continue? (y/N) ").lower()
        if response != 'y':
            sys.exit(1)

    # Check if there are uncommitted changes
    if has_uncommitted_changes(repo_path):
        print("Error: You have uncommitted changes")
        print("Please commit or stash your changes before proceeding")
        sys.exit(1)

    # Create a backup branch
    backup_branch = f"backup-before-scrub-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"Creating backup branch: {backup_branch}")
    run_command(['git', '-C', str(repo_path), 'branch', backup_branch])

    print(f"WARNING: This will rewrite Git history to remove '{file_to_remove}'")
    print(f"A backup branch has been created: {backup_branch}")
    print("This operation cannot be undone!")
    response = input("Are you sure you want to continue? (y/N) ").lower()
    if response != 'y':
        print("Operation cancelled")
        sys.exit(1)

    # Remove the file from all branches using git-filter-repo
    print(f"Removing '{file_to_remove}' from Git history...")
    run_command(['git', '-C', str(repo_path), 'filter-repo',
                '--invert-paths', '--path', file_to_remove, '--force'])

    # Clean up and optimize repository
    print("Cleaning up and optimizing repository...")
    run_command(['git', '-C', str(repo_path), 'gc', '--prune=now', '--aggressive'])

    print("\nOperation complete!")
    print(f"The file '{file_to_remove}' has been removed from all commits and branches.")
    print("\nImportant:")
    print(f"1. A backup branch has been created: {backup_branch}")
    print("2. You may need to force push these changes to remote repositories")
    print("3. Other team members will need to re-clone the repository or perform a hard reset")
    print("\nTo push these changes to remote (if needed):")
    print("git push origin --force --all")
    print("git push origin --force --tags")

if __name__ == '__main__':
    main() 