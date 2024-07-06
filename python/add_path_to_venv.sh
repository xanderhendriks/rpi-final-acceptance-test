#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(dirname $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}"))"

# Check if cygpath command exists; if yes, assume the script is being called from within MSYS
if command -v cygpath > /dev/null; then
    # Use cygpath to convert the path
    CONVERTED_PATH=$(cygpath -w -a "$SCRIPT_DIR")
else
    # If cygpath is not available, use the original path
    CONVERTED_PATH="$SCRIPT_DIR"
fi

# Get the target path using Python
TARGET_PATH="$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")/sitehive-firmware-python.pth"

# Write the converted path to the target file
echo "$CONVERTED_PATH" > "$TARGET_PATH"

echo "Path added to $TARGET_PATH"
