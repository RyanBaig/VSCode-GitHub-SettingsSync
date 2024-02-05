import json
import os
import requests
from typing import Union

class VSCode:
    """
    Base class for VSCode-related actions.
    """
    def validate_github_token(gh_token: str) -> bool:
        """
        Validate a GitHub Access Token.

        Params
        ---
            - `gh_token` (str):
                The GitHub Access Token, required.

        Returns
        ---
            - bool:
                Returns `True` if the token is valid, otherwise returns `False`.
        """

        # Set the API endpoint and headers
        url = "https://api.github.com/user"
        headers = {"Authorization": f"token {gh_token}"}

        # Make the request
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error validating GitHub Token: {e}")
            return False


    def locate_settings_file() -> Union[str, None]:
        # Default settings folder locations for different operating systems
        default_folders = {
            "darwin": os.path.expanduser("~/Library/Application Support/Code/User"),
            "linux": os.path.expanduser("~/.config/Code/User"),
            "win32": os.path.join(os.environ["APPDATA"], "Code/User"),
        }
        # Get the user's platform
        platform = os.sys.platform
        # Check if the platform is in the default_folders dictionary
        if platform in default_folders:
            vscode_settings_folder = default_folders[platform]
            # Check if the settings folder exists
            if os.path.exists(vscode_settings_folder):
                settings_file_path = os.path.join(
                    vscode_settings_folder, "settings.json"
                )
                # Check if settings.json exists
                if os.path.exists(settings_file_path):
                    with open(settings_file_path) as settings_file:
                        content = settings_file.read()
                    return content
        return None
        
    def locate_keybinds_file() -> Union[str, None]:
        # Default keybinds folder locations for different operating systems
        default_folders = {
            "darwin": os.path.expanduser("~/Library/Application Support/Code/User"),
            "linux": os.path.expanduser("~/.config/Code/User"),
            "win32": os.path.join(os.environ["APPDATA"], "Code/User"),
        }
        # Get the user's platform
        platform = os.sys.platform
        # Check if the platform is in the default_folders dictionary
        if platform in default_folders:
            vscode_keybinds_folder = default_folders[platform]
            # Check if the settings folder exists
            if os.path.exists(vscode_keybinds_folder):
                keybinds_file_path = os.path.join(
                    vscode_keybinds_folder, "keybindings.json"
                )
                # Check if settings.json exists
                if os.path.exists(keybinds_file_path):
                    with open(keybinds_file_path) as settings_file:
                        content = settings_file.read()
                    return content
        return None

    def get_extension_info(extension_path: str) -> dict:
        fields_file_path = os.path.join(extension_path, "package.json")
        try:
            if os.path.exists(fields_file_path):
                with open(
                    fields_file_path, "r", encoding="utf-8", errors="ignore"
                ) as fields_file:
                    try:
                        fields_data = json.load(fields_file)
                        # Combine publisher and name to form the extension ID
                        extension_id = f"{fields_data.get('publisher', 'N/A')}.{fields_data.get('name', 'N/A')}"
                        # Check the type of the 'repository' field
                        if isinstance(fields_data.get("repository"), dict):
                            repo_url = fields_data["repository"].get("url", "N/A")
                        else:
                            repo_url = fields_data.get("repository", "N/A")
                        return {
                            # I want the url key to have the url of the extension's page on vscode marketplace. I just need to know how I can get the extension identifier 
                            
                            "url": f"https://marketplace.visualstudio.com/items?itemName={extension_id}",
                            "version": fields_data.get("version", "N/A"),
                            "publisher": fields_data.get("publisher", "N/A"),
                            "description": fields_data.get("description", "N/A"),
                            "repository": repo_url,
                            "categories": fields_data.get("categories", []),
                        }
                    except json.JSONDecodeError as json_error:
                        print(
                            f"Error decoding JSON in {fields_file_path}: {json_error}"
                        )
                        return {
                            "version": "N/A",
                            "publisher": "N/A",
                            "description": "N/A",
                            "repository": "N/A",
                            "categories": [],
                        }
            else:
                return {
                    "version": "N/A",
                    "publisher": "N/A",
                    "description": "N/A",
                    "repository": "N/A",
                    "categories": [],
                }
        except Exception as e:
            print(f"Error processing {fields_file_path}: {e}")
            return {
                "version": "N/A",
                "publisher": "N/A",
                "description": "N/A",
                "repository": "N/A",
                "categories": [],
            }
            
    def extract_extensions_info() -> None:
        extensions_folder = os.path.join(
            os.environ["USERPROFILE"], ".vscode", "extensions"
        )
        try:
            if os.path.exists(extensions_folder):
                extensions_info = {}
                for extension_folder in os.listdir(extensions_folder):
                    extension_path = os.path.join(extensions_folder, extension_folder)
                    # Check if the entry in the folder is a directory (extension)
                    if os.path.isdir(extension_path):
                        extension_info = VSCode.get_extension_info(
                            extension_path
                        )
                        extensions_info[extension_folder] = extension_info
                # Output the extensions information to extensions-list.json
                with open(
                    "extensions-list.json", "w", encoding="utf-8"
                ) as extensions_file:
                    json.dump(
                        extensions_info, extensions_file, indent=2, ensure_ascii=False
                    )
                print(
                    "Extensions information gathered and saved to extensions-list.json."
                )
            else:
                print("Error: Extensions folder not found.")
        except Exception as e:
            print(f"Error extracting extensions information: {e}")
            