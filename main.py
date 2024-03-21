import os
from getpass import getpass

import fire

from modules.github import GitHub
from modules.variables import Variables
from modules.vscode import VSCode


class CLICommands:
    def login(self) -> str:
        print("Welcome to VSCode-Settings-Sync!")

        if not os.path.exists(os.path.join( os.path.abspath("."), ".env" )):
            print("Currently Setting Up Environment Variables...")
            with open(os.path.join( os.path.abspath("."), ".env" ), "x"):
                pass
                print("Environment Variables Successfully Setup!")
        
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


                if VSCode.validate_github_token(github_token):
                    print("Good News! The GitHub Token provided is valid! Token added to the database.")
                    # Add the token
                    Variables.put_var("GH_TOKEN", github_token)
                    break  # Exit the loop if a valid token is provided
                else:
                    print("Error: Invalid GitHub Token. Please check and try again.")
            
            attempts += 1

        if attempts == max_attempts:
            print(f"Exceeded maximum attempts ({max_attempts}). Exiting.")

    def sync_send(self):
        create_repo_process = GitHub.create_repo()
        if create_repo_process == 422:
            print("Repository Already Created, Syncing...")
        GitHub.send_files_to_repo()

    def sync_get(self):
        create_repo_process = GitHub.create_repo()
        if create_repo_process == 422:
            print("Repository Already Created, Syncing...")
        GitHub.get_files_from_repo()

if __name__ == "__main__":
    fire.Fire(CLICommands, name="ss")
