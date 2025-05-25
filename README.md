# Utility Scripts

A collection of utility scripts for common tasks.

## Prerequisites

- Python 3.8 or higher
- Poetry (Python package manager)
- Git (for Git-related scripts)

## Installation

1. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone this repository:
   ```bash
   git clone <repository-url>
   cd utility-scripts
   ```

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Scripts

### Git History Management

#### scrub-git-file
Removes a file from Git history across all branches while preserving remote references.

```bash
# Basic usage (current directory)
poetry run scrub-git-file sensitive/password.txt

# Specify a different repository
poetry run scrub-git-file -r /path/to/repo sensitive/password.txt
```

#### change-git-email
Changes email addresses in Git commit history across all branches while preserving remote references.

```bash
# Change email in current repository
poetry run change-git-email -o old@email.com -n new@email.com

# Change email in specific repository
poetry run change-git-email -r /path/to/repo -o old@email.com -n new@email.com
```

### File Format Conversion

#### csv-to-json
Converts CSV files to JSON format.

```bash
# Convert a CSV file to JSON
poetry run csv-to-json -f data.csv
```

The script will:
- Read the CSV file
- Convert it to JSON format
- Save it as a .json file in the same directory
- Preserve column headers as keys
- Strip whitespace from values

#### format-json
Formats or minifies JSON files.

```bash
# Pretty print JSON file
poetry run format-json -f data.json

# Minify JSON file
poetry run format-json -f data.json -m
```

## Development

To add new dependencies:
```bash
poetry add package-name
```

To add development dependencies:
```bash
poetry add --group dev package-name
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
