# Idea Owner
[zmarty](https://github.com/zmarty)

# CodeScore

CodeScore is a Python tool that analyzes GitHub commit diffs using Claude AI to provide detailed code quality metrics and insights. It examines various aspects of code changes including complexity, quality, type of changes, and potential technical debt.

## Features

- Fetches commit diffs from GitHub repositories
- Analyzes code changes using Claude AI
- Provides detailed metrics including:
  - Code complexity assessment
  - Code quality scoring
  - Type of changes identification
  - Test coverage detection
  - Code comment analysis
  - Programming languages used
  - Commit size evaluation
  - Technical debt assessment
  - Dependency change tracking

## Requirements

- Python 3.x
- GitHub Personal Access Token
- Claude API Key (Anthropic)
- Required Python packages:
  - requests
  - PyGithub
  - configparser

## Setup

1. Clone the repository
2. Install required packages:
```bash
pip install requests PyGithub configparser
```

3. Create a configuration file named `codescore.cfg` with the following structure:
```ini
[Github]
Token = your_github_token_here

[API]
SonnetAPIUrl = https://api.anthropic.com/v1/complete
SonnetAPIKey = your_claude_api_key_here
DiffUrl = https://api.github.com/repos/{repo_name}/compare/{previous_commit}...{latest_commit}
```

4. Create a `git.dat` file containing:
```
owner/repository_name
file_path_to_analyze
```

## Usage

1. Ensure your configuration files are properly set up
2. Run the program:
```bash
python3 codescore.py
```

The program will:
1. Fetch the commit history for the specified file
2. Get the diff between the latest and previous commit
3. Send the diff to Claude AI for analysis
4. Output a detailed JSON analysis of the code changes

## Example Output

```json
{
  "codeComplexity": {
    "value": "Low",
    "reason": "Basic logic changes were made"
  },
  "codeQuality": {
    "value": 8,
    "reason": "Code follows best practices, readable and maintainable"
  },
  "typeOfChange": {
    "value": "Refactoring",
    "reason": "Code was refactored to improve structure"
  },
  "includesTests": {
    "value": false,
    "reason": "No test changes in this commit"
  },
  // ... additional metrics
}
```

## Configuration Details

### GitHub Token
- Required permissions: repo access
- Used for accessing repository and commit information

### Claude API
- Uses Anthropic's Claude API for code analysis
- Requires a valid API key from Anthropic
- Configured to use Claude-2 model

## File Structure

- `codescore.py`: Main program file
- `codescore.cfg`: Configuration file
- `git.dat`: Repository and file information
- `prompt.dat`: Analysis prompt template

## Error Handling

The program includes error handling for:
- GitHub API access issues
- Missing or invalid configuration
- File not found scenarios
- API response errors

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
