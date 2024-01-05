from getpass import getpass

import fire

from modules.github import create_repo, sync_repo
from modules.variables import get_var, put_var
from modules.vscode import locate_settings_file, validate_github_token


class CLICommands:
    def login(self):
        print("Welcome to VSCode-GitHub-SettingsSync!")

        max_attempts = 5
        attempts = 0

        while attempts < max_attempts:
            github_token = getpass("Enter your GitHub Access Token: ")

            if len(github_token) == 0:
                print("No GitHub Token Entered, please try again.")
            elif len(github_token) != 40:
                print("Invalid GitHub Token, please try again.")
            elif len(github_token) == 40:
                # Print a masked version for verification
                print(
                    f"GitHub Token entered: {github_token[:5]}{'*' * (len(github_token) - 10)}{github_token[-5:]}"
                )

                # TODO: Validate and store the GitHub Token
                if validate_github_token(github_token):
                    print("Good News! The GitHub Token provided is valid! Token added to the database.")
                    # Use python-decouple to manage environment variables
                    # Add 'GH_TOKEN' to your .env file
                    put_var("GH_TOKEN", github_token)
                    break  # Exit the loop if a valid token is provided
                else:
                    print("Error: Invalid GitHub Token. Please check and try again.")
            
            attempts += 1

        if attempts == max_attempts:
            print(f"Exceeded maximum attempts ({max_attempts}). Exiting.")



    def sync(self):
        create_repo_process = create_repo()
        if create_repo_process == 422:
            print("Repository Already Created, Syncing...")
        sync_repo()


if __name__ == "__main__":
    fire.Fire(CLICommands, name="ss")
    # GitHubSettingsSync.extract_extensions_info()
