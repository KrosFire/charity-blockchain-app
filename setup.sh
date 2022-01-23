#!/bin/bash

# ----- Setting up needed vars -----
full_path=$(realpath $0)
dir_path=$(dirname $full_path)
export PYTHONPATH="$dir_path/src"

# ----- Installing needed dependencies -----
pip install -r requirements.txt

