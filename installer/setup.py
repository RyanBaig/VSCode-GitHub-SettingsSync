import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "includes": [],  # Add any additional modules your application depends on
    "packages": ["ttkbootstrap"],  # Add any packages here if needed
    "excludes": [],
    "include_files": [],  # Add any additional files or data here
}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Executable
executables = [
    Executable("C:\\Users\\Hp\\Projects\\Python\\VSCode-Settings-Sync\\installer\\installer.py", base=base)
]

# Setup
setup(
    name="VSCode-Settings-Sync Installer",
    version="1.0",
    description="",
    options={"build_exe": build_exe_options},
    executables=executables
)
