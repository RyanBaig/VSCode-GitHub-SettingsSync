import os
import platform
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

from ttkbootstrap import Style


# Function to perform installation
def install_vscss():
    # Define the GitHub repository and installation directory
    github_repo = "https://github.com/RyanBaig/VSCode-Settings-Sync.git"
    install_dir = os.path.join(os.path.expanduser("~"), "VSCode-Settings-Sync")

    try:
        # Check if the installation directory already exists; if it does, remove it
        if os.path.exists(install_dir):
            status_label.config(text="Removing existing installation directory.")
            if platform.system() == "Windows":
                subprocess.call(["rmdir", "/s", "/q", install_dir], shell=True)
            else:
                subprocess.call(["rm", "-rf", install_dir])

        # Update the status label and start the progress bar
        status_label.config(text="Cloning the repository into TerminalTools directory.")
        progress["value"] = 0  # Reset progress bar to 0
        progress.start()

        # Clone the GitHub repository into the installation directory
        subprocess.call(["git", "clone", github_repo, install_dir])

        # Stop the progress bar
        progress.stop()

        # Add installation directory to PATH if on Windows
        if platform.system() == "Windows":
            path_env = os.environ["PATH"]
            path_env += os.pathsep + install_dir
            os.environ["PATH"] = path_env
            # Save the changes to the PATH environment variable
            os.system('setx PATH "{}"'.format(path_env))

        elif platform.system() == "Linux":
            # Get the current value of PATH
            directory = install_dir
            current_path = os.environ.get("PATH", "")

            # Add the directory to PATH if it's not already there
            if directory not in current_path.split(os.pathsep):
                os.environ["PATH"] = f"{directory}{os.pathsep}{current_path}"

            # Save the updated PATH in the user's shell configuration file
            with open(os.path.expanduser("~/.bashrc"), "a") as file:
                file.write(
                    f"\n# Added by VSCode-Settings-Sync Installer\nexport PATH={directory}:${{PATH}}\n"
                )

        status_label.config(
            text="VSCode-Settings-Sync has been installed and added to the PATH."
        )
        progress["value"] = (
            100  # Set the progress bar to 100% when installation is complete
        )
        if platform.system() == "Linux":
            os.chmod(os.path.join(install_dir, "ss.sh"), 0o775)
        else:
            pass
    except Exception as e:
        status_label.config(text=f"An error occurred: {str(e)}")


def start_installation_thread():
    install_button.configure(state="disabled")
    installation_thread = threading.Thread(target=install_vscss)
    installation_thread.start()


# Create the main window
root = tk.Tk()
root.title("VSCode-Settings-Sync Installer")
root.geometry("500x200")

# Use ttkbootstrap styles
style = Style(theme="darkly")
root.style = style

# Create a label
label = ttk.Label(
    root,
    text="Click the 'Install' button to install VSCode-Settings-Sync",
    font=("Helvetica", 15),
)
label.pack(pady=10)

# Create the 'Install' button
install_button = ttk.Button(root, text="Install", command=start_installation_thread)
install_button.pack()

# Create a label to display installation status
status_label = ttk.Label(root, text="")
status_label.pack(pady=10)

# Create a progress bar
progress = ttk.Progressbar(root, mode="determinate", length=300)
progress.pack(pady=10)

# Start the GUI
root.mainloop()
