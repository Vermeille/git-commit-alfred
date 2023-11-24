#!/bin/bash

wget https://raw.githubusercontent.com/Vermeille/git-commit-alfred/master/src/commit-msg -O .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
wget https://raw.githubusercontent.com/Vermeille/git-commit-alfred/master/src/prepare-commit-msg -O .git/hooks/prepare-commit-msg
chmod +x .git/hooks/prepare-commit-msg
wget https://raw.githubusercontent.com/Vermeille/git-commit-alfred/master/src/gigaprompt.py -O .git/hooks/gigaprompt.py
chmod +x .git/hooks/gigaprompt.py
