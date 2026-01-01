import os
import base64
import requests
from dotenv import load_dotenv
load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_PAT = os.getenv("GITHUB_PAT")

BASE_URL = "https://api.github.com"

headers = {
    "Authorization": f"Bearer {GITHUB_PAT}",
    "Accept": "application/vnd.github+json"
}

def create_repo(repo_name, description="", private=True):
    url = f"{BASE_URL}/user/repos"
    data = {
        "name": repo_name,
        "description": description,
        "private": private
    }
    resp = requests.post(url, json=data, headers=headers)
    return resp.json()

def create_or_update_file(repo_name, file_path, content, commit_message="Add file"):
    url = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_path}"

    # Encode file content to Base64 as GitHub requires
    encoded_content = base64.b64encode(content.encode()).decode()

    # Check if file exists (get SHA if yes)
    get_file = requests.get(url, headers=headers)
    sha = get_file.json().get("sha") if get_file.status_code == 200 else None

    data = {
        "message": commit_message,
        "content": encoded_content,
    }

    if sha:
        data["sha"] = sha

    resp = requests.put(url, json=data, headers=headers)
    return resp.json()

def get_file(repo_name, file_path):
    url = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_path}"
    resp = requests.get(url, headers=headers)
    return resp.json()
