@echo off

set "abs_path=%~dp0main.py"

set "packages=%~dp0requirements.txt"

pip install -r %packages%

python %abs_path% %*