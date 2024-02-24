try:
    import os
    import subprocess
    import threading
    import tkinter as tk
    from tkinter import ttk

    from ttkbootstrap import Style

    # Function to perform installation
    def install_vscss():
        # Define the GitHub repository and installation directory
        github_repo = 'https://github.com/RyanBaig/VSCode-Settings-Sync.git'
        install_dir = os.path.join(os.environ['APPDATA'], 'VSCode-Settings-Sync')

        
        try:
            # Check if the installation directory already exists; if it does, remove it
            if os.path.exists(install_dir):
                status_label.config(text="Removing existing installation directory.")
                subprocess.call(['rmdir', '/s', '/q', install_dir], shell=True)

            # Update the status label and start the progress bar
            status_label.config(text="Cloning the repository into Program Files.")
            progress["value"] = 0  # Reset progress bar to 0
            progress.start()

            # Clone the GitHub repository into the installation directory
            subprocess.call(['git', 'clone', github_repo, install_dir])

            # Stop the progress bar
            progress.stop()

            path_env = os.environ['PATH']
            path_env += os.pathsep + install_dir
            os.environ['PATH'] = path_env

            # Save the changes to the PATH environment variable
            # This is specific to Windows, modify it accordingly for other operating systems
            os.system('setx PATH "{}"'.format(path_env))

            status_label.config(text="VSCode-Settings-Sync has been installed and added to the PATH.")
            progress["value"] = 100  # Set the progress bar to 100% when installation is complete
        except Exception as e:
            status_label.config(text=f"An error occurred: {str(e)}")

    def start_installation_thread():
        install_button.configure(state="disabled")
        installation_thread = threading.Thread(target=install_vscss)
        installation_thread.start()

    # Create the main window
    root = tk.Tk()
    root.title("TerminalTools Installer")
    root.geometry("500x200")

    
    # Use ttkbootstrap styles
    style = Style(theme='darkly')
    root.style = style

    # Create a label
    label = ttk.Label(root, text="Click the 'Install' button to install VSCode-Settings-Sync", font=("Helvetica", 15))
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
except KeyboardInterrupt:
    pass
