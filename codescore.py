import requests
import configparser
import os
import base64
import json
from github import Github

# Read configuration parameters from Codescore.cfg
config = configparser.ConfigParser()
config.read('codescore.cfg')

GITHUB_TOKEN = config['Github']['Token']
SONNET_API_URL = config['API']['SonnetAPIUrl']
SONNET_API_KEY = config['API']['SonnetAPIKey']
DIFF_URL_TEMPLATE = config['API']['DiffUrl']

# Read repository and file names from git.dat
git_dat_file = 'git.dat'
with open(git_dat_file, 'r') as file:
    repo_name = file.readline().strip()
    file_path = file.readline().strip()

# GitHub setup
g = Github(GITHUB_TOKEN)
repo = g.get_repo(repo_name)

# Get the commit history for the specified file
commits = repo.get_commits(path=file_path)
latest_commit = commits[0]
previous_commit = commits[1]

diff_url = DIFF_URL_TEMPLATE.format(repo_name=repo_name, previous_commit=previous_commit.sha, latest_commit=latest_commit.sha)
headers = {'Authorization': f'token {GITHUB_TOKEN}'}
response = requests.get(diff_url, headers=headers)

if response.status_code != 200:
    print("Error fetching the diff from GitHub")
    exit()

diff_data = response.json().get('files', [])
diff = ""
for file in diff_data:
    if file['filename'] == file_path:
        diff = file['patch']
        break

if not diff:
    print("No diff found for the specified file")
    exit()

# Read prompt from prompt.dat in current directory
prompt_file = 'prompt.dat'
with open(prompt_file, 'r') as file:
    prompt_template = file.read()

# Format the prompt with the commit message and diff
formatted_prompt = prompt_template.replace("{{message}}", latest_commit.commit.message)
formatted_prompt = formatted_prompt.replace("{{diff | truncate: 100000}}", diff)

# Split the prompt into system and human parts
system_prompt = formatted_prompt.split("--- user")[0].strip()
user_prompt = formatted_prompt.split("--- user")[1].strip()

# Format the prompt according to Anthropic's requirements
final_prompt = f"{system_prompt}\n\nHuman: {user_prompt}\n\nAssistant:"

# Prepare the data for Anthropic API
anthropic_payload = {
    "prompt": final_prompt,
    "model": "claude-2",
    "max_tokens_to_sample": 1000,
    "temperature": 0,
    "stop_sequences": ["\n\nHuman:"]
}

headers = {
    "x-api-key": SONNET_API_KEY,
    "Content-Type": "application/json",
    "anthropic-version": "2023-06-01"
}

# Send the request to Anthropic API
response = requests.post(SONNET_API_URL, json=anthropic_payload, headers=headers)

if response.status_code == 200:
    # Extract and parse the JSON from the completion
    completion = response.json()['completion']
    start = completion.find('{')
    end = completion.rfind('}') + 1
    json_str = completion[start:end]
    
    # Pretty print the JSON
    analysis = json.loads(json_str)
    print("\nCode Analysis Results:")
    print(json.dumps(analysis, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
