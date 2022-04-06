#!/bin/bash

echo "Creating venv..."
mkdir venv
python3 -m venv ./venv

echo "Installing modules..."
source ./venv/bin/activate
pip install pygame

deactivate
echo "Done!"
