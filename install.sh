#!/bin/bash

echo "Creating a new Conda environment..."
conda create -n eAI -c conda-forge python=3.12 -y

echo "Activating the new Conda environment..."
conda activate eAI

echo "Installing the Python requirements..."
pip install -r requirements.txt

echo "Downloading the SpaCy NLP model..."
python -m spacy download en_core_web_sm

echo "Installation completed."
read -p "Press enter to continue"