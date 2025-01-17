## Badges

![License](https://badgers.space/github/license/RyanBaig/VSCode-Settings-Sync/) ![Open Issues](https://badgers.space/github/open-issues/RyanBaig/VSCode-Settings-Sync)

## VSCode-Settings-Sync

VSCode-SettingsSync is a Python-based command-line tool designed to streamline the synchronization of Visual Studio Code settings and installed extensions across multiple development environments. The project leverages GitHub as a central repository to store and version control VSCode settings, allowing developers to effortlessly maintain a consistent and personalized development environment.

> [!IMPORTANT]
 _Please note, that this **ONLY** syncronizes VSCode Settings, Keybinds and Extensions._

### Key Features:

1. GitHub Integration: Utilizes GitHub repositories to store and synchronize VSCode settings and extensions.

2. Settings Sync: Facilitates the seamless transfer of VSCode settings, ensuring a consistent development environment across different machines.

3. Extension Management: Gathers information about installed extensions and syncs the data with the GitHub repository.

4. Keybinds Saving: Automatically saves keybinds to the GitHub repository, ensuring they are always up-to-date.
5. Secure: Ensures the privacy of sensitive information by using private GitHub repositories and access tokens.

6. User-Friendly CLI: Offers a straightforward command-line interface for easy setup and synchronization.

### How to Use:
- Install the CLI using the [Installer](./installer.tar.gz)
- Run the tool's CLI commands to log in with a GitHub Access Token. (`bash ss.sh login`)
- Create a private GitHub repository for VSCode settings using the provided commands. (Automatically created)
- Sync VSCode settings and installed extensions across devices effortlessly.

## Installation

To Use/Install this project, follow the given steps:

1. Clone the Repo:

```bash
git clone https://github.com/RyanBaig/VSCode-Settings-Sync.git
```


1. Generate a [GitHub Access Token](https://github.com/settings/tokens) with `delete_repo` and all `repo` perms.
![Token Perms IMG 1](./screenshots/token-perms1.JPG)
![Token Perms IMG 2](./screenshots/token-perms2.JPG)

1. Open the Terminal, type `ss login`, provide your GitHub Access Token.

2. To Sync your settings and extensions to the repository, type `ss sync-send` to save your current settings to the repository or use `ss sync-get` to get the settings from the repository.
