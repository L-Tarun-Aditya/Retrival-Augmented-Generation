#!/bin/bash

# Set PYTHONPATH to include src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

echo "Starting RAG API server..."
echo "PYTHONPATH: $PYTHONPATH"

cd src/api
python3 server.py
