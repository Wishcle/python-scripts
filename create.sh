#!/usr/bin/env bash

set -euo pipefail

print_usage_and_exit() {
    echo "Create a new Python package based on the 'template' directory."
    echo ""
    echo "Usage: $0 [--help | -h] (--name | -n) <package_name>"
    exit 1
}

PKG_NAME=""

# CLI.
while [[ $# -gt 0 ]]; do
    case "$1" in
        -n|--name)
            PKG_NAME="$2"
            shift 2
            ;;
        -h|--help)
            print_usage_and_exit
            ;;
        *)
            echo "Unknown option: $1"
            print_usage_and_exit
            ;;
    esac
done

if [[ -z "$PKG_NAME" ]]; then
    echo "Error: Package name is required."
    print_usage_and_exit
fi

# Validate package name (according to `uv init _test` error output).
if [[ ! "$PKG_NAME" =~ ^[a-z0-9]([a-zA-Z0-9._-]*[a-z0-9])?$ ]]; then
    echo \
        "Error: '$PKG_NAME' is not a valid Python package name. " \
        "Names must start and end with a letter or digit and may only " \
        "contain -, _, ., and alphanumeric characters."
    exit 1
fi

if [ -d "$PKG_NAME" ]; then
    echo "Error: '$PKG_NAME' directory already exists! Will not overwrite."
    exit 1
fi

if [ ! -d "template" ]; then
    echo "Error: 'template' directory not found."
    exit 1
fi

TARGET_DIR="$PKG_NAME"
cp -r "template" "$TARGET_DIR"

# Replace "template" with "$PKG_NAME" in file/directory names.
find "$TARGET_DIR" -depth -name '*template*' | while read -r path; do
    new_path="${path//template/$PKG_NAME}"
    mv "$path" "$new_path"
done

# Replace "template" with "$PKG_NAME" inside files.
find "$TARGET_DIR" -type f -exec sed -i "s/template/$PKG_NAME/g" {} +

echo "Success: Package structure created under ./$TARGET_DIR/"
