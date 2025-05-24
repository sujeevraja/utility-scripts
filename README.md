# Utility Scripts

A collection of utility scripts for common tasks.

## Prerequisites

- Python 3.x
- Git (for Git-related scripts)
- git-filter-repo (for Git history modification scripts)
  ```bash
  pip3 install git-filter-repo
  ```

## Scripts

### Git History Management

#### scrub_file_from_git_history.py
Removes a file from Git history across all branches while preserving remote references.

```bash
# Basic usage (current directory)
./scrub_file_from_git_history.py sensitive/password.txt

# Specify a different repository
./scrub_file_from_git_history.py -r /path/to/repo sensitive/password.txt
```

#### change_git_emails.py
Changes email addresses in Git commit history across all branches while preserving remote references.

```bash
# Change email in current repository
./change_git_emails.py -o old@email.com -n new@email.com

# Change email in specific repository
./change_git_emails.py -r /path/to/repo -o old@email.com -n new@email.com

# Change both email and name
./change_git_emails.py -o old@email.com -n new@email.com -N "New Name"
```

### File Format Conversion

#### csv_to_json.py
Converts CSV files to JSON format.

```bash
# Convert a CSV file to JSON
./csv_to_json.py -f data.csv
```

The script will:
- Read the CSV file
- Convert it to JSON format
- Save it as a .json file in the same directory
- Preserve column headers as keys
- Strip whitespace from values

#### format_json.py
Formats or minifies JSON files.

```bash
# Pretty print JSON file
./format_json.py -f data.json

# Minify JSON file
./format_json.py -f data.json -m
```

## Common Features

All scripts include:
- Error handling with descriptive messages
- Command-line argument parsing
- Logging of operations
- Safety checks before destructive operations

## Safety Notes

For Git history modification scripts:
1. Always create a backup before running
2. Be aware that history rewriting affects all branches
3. Force push will be required after changes
4. Other team members will need to re-clone or perform a hard reset

## License

See [LICENSE](LICENSE) file for details.
