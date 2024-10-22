#!/bin/bash

# Specify the module directory
MODULE_DIR="/path/to/module" # Set your module directory here

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
   echo "Usage: $0 <src_dir> <dest_dir>"
   exit 1
fi

# Assign arguments to variables
SOURCE_DIR="$1"
DESTINATION_DIR="$2"

# Call the Python script to copy files with newer timestamps
python3 - <<EOF
import sys
import os

# Add module directory to sys.path if it's not already present
if os.path.abspath('${MODULE_DIR}') not in sys.path:
    sys.path.append(os.path.abspath('${MODULE_DIR}'))

from file import copy_files_with_newer_timestamps

# Call the function with the provided source and destination directories
copy_files_with_newer_timestamps('${SOURCE_DIR}', '${DESTINATION_DIR}')
EOF

# Usage examples
cat <<EOF
Usage examples:
1. To copy files from /home/user/source to /home/user/destination:
   ./copy_files.sh /home/user/source /home/user/destination
EOF
