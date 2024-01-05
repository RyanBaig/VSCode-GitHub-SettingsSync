
## Badges

![License](https://badgers.space/github/license/RyanBaig/VSCode-GitHub-SettingsSync/)

![Open Issues](https://badgers.space/github/open-issues/RyanBaig/VSCode-GitHub-SettingsSync)
## VSCode-GitHub-SettingsSync 

VSCode-GitHub-SettingsSync is a Python-based command-line tool designed to streamline the synchronization of Visual Studio Code settings and installed extensions across multiple development environments. The project leverages GitHub as a central repository to store and version control VSCode settings, allowing developers to effortlessly maintain a consistent and personalized development environment.
*Please note, that this **ONLY** syncronizes VSCode Settings and Extensions.* 

### Key Features:


1. GitHub Integration: Utilizes GitHub repositories to store and synchronize VSCode settings and extensions.

2. Settings Sync: Facilitates the seamless transfer of VSCode settings, ensuring a consistent development environment across different machines.

3. Extension Management: Gathers information about installed extensions and syncs the data with the GitHub repository.

4. Secure: Ensures the privacy of sensitive information by using private GitHub repositories and access tokens.

5. User-Friendly CLI: Offers a straightforward command-line interface for easy setup and synchronization.

### How to Use:

- Run the tool's CLI commands to log in with a GitHub Access Token.
- Create a private GitHub repository for VSCode settings using the provided commands.
- Sync VSCode settings and installed extensions across devices effortlessly.

## Installation

To Use/Install this project, follow the given steps:

1. Clone the Repo:
```bash
git clone https://github.com/RyanBaig/VSCode-GitHub-SettingsSync.git
```

2. Make a `.env` file.

3. Generate a [GitHub Access Token](https://github.com/settings/tokens) with `delete_repo` and all `repo` perms.

4. Open the Terminal, type `ss login`, provide your GitHub Access Token.

5. To Sync your settings and extensions to the repository, type `ss sync`
    