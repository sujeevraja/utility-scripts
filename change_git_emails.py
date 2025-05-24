#!/usr/bin/env python3

"""
Script to change email addresses in Git commit history.
"""

import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from common import ScriptException

def run_command(cmd, check=True):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise ScriptException(f"Error executing command: {' '.join(cmd)}\nError message: {e.stderr}")

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

def get_remotes(path):
    """Get list of remote names in the repository."""
    try:
        result = subprocess.run(['git', '-C', path, 'remote'],
                              check=True, capture_output=True, text=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        return []

def main():
    try:
        parser = argparse.ArgumentParser(
            description='Change email addresses in Git commit history',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s -r /path/to/repo -o old@email.com -n new@email.com  # Change email in specific repo
  %(prog)s -o old@email.com -n new@email.com                  # Change email in current repo

Note: This script requires git-filter-repo to be installed
      Install with: pip3 install git-filter-repo
            """
        )
        parser.add_argument('-r', '--repo', default='.',
                          help='Path to the Git repository (default: current directory)')
        parser.add_argument('-o', '--old-email', required=True,
                          help='Old email address to replace')
        parser.add_argument('-n', '--new-email', required=True,
                          help='New email address to use')
        parser.add_argument('-N', '--new-name', default=None,
                          help='New name to use (optional)')
        args = parser.parse_args()

        # Check if git-filter-repo is installed
        try:
            subprocess.run(['git-filter-repo', '--version'],
                          check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise ScriptException("git-filter-repo is not installed\nPlease install it with: pip3 install git-filter-repo")

        repo_path = Path(args.repo).resolve()
        old_email = args.old_email
        new_email = args.new_email
        new_name = args.new_name

        # Check if repository path exists
        if not repo_path.is_dir():
            raise ScriptException(f"Repository path does not exist: {repo_path}")

        # Check if we're in a git repository
        if not is_git_repo(repo_path):
            raise ScriptException(f"Not in a Git repository: {repo_path}")

        # Get list of remotes before making changes
        remotes = get_remotes(repo_path)
        if not remotes:
            print("Warning: No remotes found in the repository")

        # Check if there are uncommitted changes
        if has_uncommitted_changes(repo_path):
            raise ScriptException("You have uncommitted changes\nPlease commit or stash your changes before proceeding")

        # Create a backup branch
        backup_branch = f"backup-before-email-change-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        print(f"Creating backup branch: {backup_branch}")
        run_command(['git', '-C', str(repo_path), 'branch', backup_branch])

        print(f"WARNING: This will rewrite Git history to change email from '{old_email}' to '{new_email}'")
        if new_name:
            print(f"and name to '{new_name}'")
        print(f"A backup branch has been created: {backup_branch}")
        print("This operation cannot be undone!")
        response = input("Are you sure you want to continue? (y/N) ").lower()
        if response != 'y':
            print("Operation cancelled")
            sys.exit(1)

        # Build the git filter-repo command
        cmd = ['git', '-C', str(repo_path), 'filter-repo',
               '--email-callback', f"return b'{new_email}' if email == b'{old_email}' else email",
               '--preserve-refs',  # Preserve remote references
               '--force']

        # Add name change if specified
        if new_name:
            cmd.extend(['--name-callback', f"return b'{new_name}' if name == b'{old_email.split('@')[0]}' else name"])

        # Change the email in all commits
        print(f"Changing email from '{old_email}' to '{new_email}'...")
        run_command(cmd)

        # Clean up and optimize repository
        print("Cleaning up and optimizing repository...")
        run_command(['git', '-C', str(repo_path), 'gc', '--prune=now', '--aggressive'])

        print("\nOperation complete!")
        print(f"Email has been changed from '{old_email}' to '{new_email}' in all commits.")
        if new_name:
            print(f"Name has been changed to '{new_name}' in all commits.")
        print("\nImportant:")
        print(f"1. A backup branch has been created: {backup_branch}")
        print("2. You may need to force push these changes to remote repositories")
        print("3. Other team members will need to re-clone the repository or perform a hard reset")
        print("\nTo push these changes to remote (if needed):")
        print("git push origin --force --all")
        print("git push origin --force --tags")

    except ScriptException as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 