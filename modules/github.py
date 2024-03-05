import base64
import os
import time
from datetime import datetime
import requests
from modules.variables import Variables
from modules.vscode import VSCode
from typing import Union
import subprocess
import json
import urllib.parse
from pathlib import Path

class GitHub:
    """
    Base class for GitHub-related actions.
    """
    def create_repo(self) -> int:
        """
        Creates a new GitHub repository for syncing.
        """
        url = "https://api.github.com/user/repos"
        token = Variables.get_var("gh_token")
        
        try:
            user_info = requests.get("https://api.github.com/user", headers={
                "Authorization": f"token {token}"
                }).json()
            name = user_info.get("login", None)
        except KeyError:
            print("Invalid GitHub Token, do `ss login` again to reverify the token.")
            return 401  # Return an appropriate status code for an invalid token

        repo_name = None or f"{name}-VSCode-Settings-Sync"

        body = {
            "name": repo_name,
            "description": "A repository for storing your VSCode settings",
            "homepage": "https://github.com/RyanBaig/VSCode-Settings-Sync",
            "private": True,
            "auto_init": True,  # Initialize with a README
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
                return self.create_repo() # Return the result of the recursive call
            else:
                print(f"Error creating repository. Status code: {r.status_code}")

                # Attempt to extract GitHub API error details from the response
                try:
                    error_message = r.json().get("message", "Unknown error")
                    print(f"GitHub API error details: {error_message}")
                except ValueError:
                    print("Unable to parse GitHub API error details from the response.")

            return r.status_code

        except requests.exceptions.HTTPError as http_error:
            if http_error.response.status_code == 401:
                print("Unauthorized access. Please check your GitHub token.")
            else:
                print(f"HTTP error: {http_error.response.status_code}")
            return http_error.response.status_code

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return 500  # You can choose an appropriate status code for request-related errors

        except Exception as e:
            print(f"Unexpected error: {e}")
            return 500  # You can choose an appropriate status code for unexpected errors

    def send_files_to_repo(self) -> None:
        """Send setting files (settings.json, extensions-list.json, keybindings.json) to the rpeository."""
        # Put settings.json and extensions-list.json into same dir as script
        # 1. Settings
        settings_content = VSCode.locate_settings_file()
        settings_file_path = os.path.abspath("./settings.json")
        with open(settings_file_path, "w") as file:
            file.write(settings_content)
        
        # 2. Extensions
        VSCode.extract_extensions_info()
        extensions_file_path = os.path.abspath("./extensions-list.json")

        # 3. Keybinds
        keybinds_content = VSCode.locate_keybinds_file()
        keybinds_file_path = os.path.abspath("./keybinds.json")
        with open(keybinds_file_path, "w") as file:
            file.write(keybinds_content)

        # Load GitHub token from environment variables
        github_token = Variables.get_var("GH_TOKEN")

        # Repository details
        repo_owner = requests.get("https://api.github.com/user", headers={"Authorization": f"token {github_token}"}).json()["login"]
        repo_name = f"{repo_owner}-VSCode-Settings-Sync"  # Replace with your repository name

        # GitHub API URLs
        repo_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/"
        settings_url = repo_url + "settings.json"
        extensions_url = repo_url + "extensions-list.json"
        keybinds_url = repo_url + "keybinds.json"

        # Headers with authorization
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        try:
            # Function to upload a file to GitHub repository
            def upload_file(file_path: str, target_url: str) -> None:
                """Helper function for `send_files_to_repo` to upload files."""
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
            def get_existing_file_sha(target_url: str) -> Union[str, None]:
                """Get the SHA for the existing setting files."""
                response = requests.get(target_url, headers=headers)
                
                if response.status_code == 200:
                    return response.json().get("sha")

                return None


            # Upload settings.json
            upload_file(settings_file_path, settings_url)

            # Upload extensions-list.json
            upload_file(extensions_file_path, extensions_url)

            # Upload keybinds.json
            upload_file(keybinds_file_path, keybinds_url)

        except requests.exceptions.RequestException as e:
            print(f"Error during sync: {e}")

    def get_files_from_repo(self) -> None:
        """Get setting files (settings.json, extensions-list.json, keybindings.json) from the rpeository."""
        # Load GitHub token from environment variables
        github_token = Variables.get_var("GH_TOKEN")

        # Repository details
        user_info = requests.get("https://api.github.com/user", headers={"Authorization": f"token {github_token}"}).json()
        repo_owner = user_info.get("login", None)
        repo_name = None or f"{repo_owner}-VSCode-Settings-Sync"  # Replace with your repository name

        # GitHub API URLs
        if repo_name is not None:
            repo_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/"
            settings_url = repo_url + "settings.json"
            extensions_url = repo_url + "extensions-list.json"
            keybinds_url = repo_url + "keybinds.json"

            # Headers with authorization
            headers = {
                "Authorization": f"Bearer {github_token}",
                "Accept": "application/vnd.github.v3+json",
            }

            def download_file(file_url: str, target_path: str) -> None:
                """Helper function for `get_files_from_repo` to download files."""
                response = requests.get(file_url, headers=headers)
                response.raise_for_status()

                # Decode content and handle encoding issues
                try:
                    content = base64.b64decode(response.json()["content"]).decode("utf-8")
                except UnicodeDecodeError as e:
                    print(f"UnicodeDecodeError: {e}")
                    content = base64.b64decode(response.json()["content"]).decode("utf-8", errors="replace")

                # Write to the target file with utf-8 encoding using writebytes
                with open(target_path, 'wb') as file:
                    file.write(content.encode("utf-8"))

                print(f"File downloaded successfully to {target_path}")

            def install_extensions_from_list(extension_list_path):
                with open(extension_list_path, 'r') as file:
                    extensions_data = json.load(file)

                # Construct a list of extension installation commands
                extension_commands = []
                for _, extension_info in extensions_data.items():
                    extension_url = extension_info['url']
                    extension_name = urllib.parse.unquote(extension_url.split("itemName=")[-1])
                    extension_commands.append(f"code --install-extension {extension_name}")

                # Join all commands into a single long command
                command = " && ".join(extension_commands)

                # Execute the single long command
                subprocess.run(command, shell=True)

            try:
                # Determine the user's home directory
                home_dir = Path.home()

                # Set the paths for settings, extensions, and keybindings
                settings_target_path = home_dir / ".config" / "Code" / "User" / "settings.json"
                extensions_target_path = Path.home() / "Desktop" / "extensions-list.json"
                keybinds_target_path = home_dir / ".config" / "Code" / "User" / "keybindings.json"

                # Download settings.json
                download_file(settings_url, settings_target_path)

                # Download extensions-list.json to the user's desktop
                download_file(extensions_url, extensions_target_path)

                # Download keybinds.json
                download_file(keybinds_url, keybinds_target_path)

                # Install the VSCode extensions
                install_extensions_from_list(extensions_target_path)            

            except requests.exceptions.RequestException as e:
                print(f"Error during file retrieval: {e}")
