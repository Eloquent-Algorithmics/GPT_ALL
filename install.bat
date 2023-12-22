@echo off

echo Creating a new Conda environment...
call conda create -n ksGPT -c conda-forge python=3.12 -y

echo Activating the new Conda environment...
call conda activate ksGPT

echo Installing the Python requirements...
call pip install -r requirements.txt

echo Downloading the SpaCy NLP model...
call python -m spacy download en_core_web_sm

echo Installation completed.