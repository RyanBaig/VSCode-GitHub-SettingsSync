import base64
import os
import time
from datetime import datetime

import requests

from modules.variables import get_var
from modules.vscode import extract_extensions_info, locate_settings_file


def create_repo():
    url = "https://api.github.com/user/repos"
    token = get_var("gh_token")
    name = requests.get("https://api.github.com/user", headers={"Authorization": f"token {token}"}).json()["login"]
    repo_name = f"{name}-VSCode-Settings-Sync"

    body = {
        "name": repo_name,
        "description": "A repository for storing your VSCode settings",
        "homepage": f"https://github.com/RyanBaig/VSCode-GitHub-SettingsSync",
        "private": True,
        "auto_init": True,  # Initialize with a README
        "license_template": "mit",  # Specify the license (optional)
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",  # Specify API version
    }

    try:
        r = requests.post(url, json=body, headers=headers)
        r.raise_for_status()  # Raise HTTPError for bad responses

        # Check if the repository was successfully created
        if r.status_code == 201:
            print("Repository created successfully!")
        elif r.status_code == 422:
           reset_time = int(r.headers["X-RateLimit-Reset"])
           print(f"Rate limit exceeded. Reset time: {reset_time}")
           print("Retrying create_repo process after reset time...")
           time.sleep(reset_time - int(time.time()))
           create_repo()
        else:
            print(f"Error creating repository. Status code: {r.status_code}")

            # Attempt to extract GitHub API error details from the response
            try:
                error_message = r.json().get("message", "Unknown error")
                print(f"GitHub API error details: {error_message}")
            except ValueError:
                print("Unable to parse GitHub API error details from the response.")

        return r.status_code

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        print(f"Error while sending request: {e}")
        return 500  # You can choose an appropriate status code for request-related errors

    except Exception as e:
        # Handle other exceptions
        print(f"Unexpected error: {e}")
        return 500  # You can choose an appropriate status code for unexpected errors

def send_files_to_repo():
    # Assuming settings.json and extensions-list.json are in the same directory as this script
    settings_content = locate_settings_file()
    settings_file_path = os.path.abspath("./settings.json")
    with open(settings_file_path, "w") as file:
        file.write(settings_content)
    
    extract_extensions_info()
    extensions_file_path = os.path.abspath("./extensions-list.json")

    # Load GitHub token from environment variables
    github_token = get_var("GH_TOKEN")

    # Repository details
    repo_owner = requests.get("https://api.github.com/user", headers={"Authorization": f"token {github_token}"}).json()["login"]
    repo_name = f"{repo_owner}-VSCode-Settings-Sync"  # Replace with your repository name

    # GitHub API URLs
    repo_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/"
    settings_url = repo_url + "settings.json"
    extensions_url = repo_url + "extensions-list.json"

    # Headers with authorization
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        # Function to upload a file to GitHub repository
        def upload_file(file_path, target_url):
            with open(file_path, "rb") as file:
                content = file.read()
                encoded_content = base64.b64encode(content).decode("utf-8")

            # Check if the file already exists
            existing_file_sha = get_existing_file_sha(target_url)

            body = {
                "message": f"Syncing VSCode settings ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
                "content": encoded_content,
            }

            # If the file exists, include the SHA of the existing file in the request
            if existing_file_sha:
                body["sha"] = existing_file_sha

            response = requests.put(target_url, headers=headers, json=body)
            response.raise_for_status()
            os.remove(file_path)
            print(f"File {file_path} uploaded successfully!")

        # Function to get the SHA of an existing file
        def get_existing_file_sha(target_url):
            response = requests.get(target_url, headers=headers)
            
            if response.status_code == 200:
                return response.json().get("sha")

            return None


        # Upload settings.json
        upload_file(settings_file_path, settings_url)

        # Upload extensions-list.json
        upload_file(extensions_file_path, extensions_url)

    except requests.exceptions.RequestException as e:
        print(f"Error during sync: {e}")

def get_files_from_repo():
    # Load GitHub token from environment variables
    github_token = get_var("GH_TOKEN")

    # Repository details
    repo_owner = requests.get("https://api.github.com/user", headers={"Authorization": f"token {github_token}"}).json()["login"]
    repo_name = f"{repo_owner}-VSCode-Settings-Sync"  # Replace with your repository name

    # GitHub API URLs
    repo_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/"
    settings_url = repo_url + "settings.json"
    extensions_url = repo_url + "extensions-list.json"

    # Headers with authorization
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    def download_file(file_url, target_path):
        
        response = requests.get(file_url, headers=headers)
        response.raise_for_status()

        # Decode content and write to the target file
        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        with open(target_path, "w") as file:
            file.write(content.replace("\U0001f4f7", ""))

        print(f"File downloaded successfully to {target_path}")
    try:
        # Specify dynamic target paths for each file
        # what is the path to vscode settings.json? ans: 
        settings_target_path = os.path.join(os.environ["APPDATA"], "Code", "User", "settings.json")
        extensions_target_path = os.path.join(os.path.expanduser("~"), "Desktop", "extensions-list.json")

        # Download settings.json
        download_file(settings_url, settings_target_path)

        # Download extensions-list.json to the user's desktop
        download_file(extensions_url, extensions_target_path)

    except requests.exceptions.RequestException as e:
        print(f"Error during file retrieval: {e}")
