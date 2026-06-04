#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_PYTHON="$DIR/.miniforge3/envs/lazymouse/bin/python3"

if [ ! -f "$ENV_PYTHON" ]; then
    echo "Error: Conda environment not found."
    echo "Run ./setup.sh first to create it."
    exit 1
fi

exec "$ENV_PYTHON" "$DIR/main.py"
