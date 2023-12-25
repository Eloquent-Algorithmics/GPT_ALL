
# Use the official Miniconda image as a parent image
FROM mcr.microsoft.com/devcontainers/miniconda:0-3

# Set the working directory in the container
WORKDIR /workspace

# Initialize conda for shell interaction
RUN conda init

# Create a new Conda environment named ksGPT with Python 3.12
RUN conda create -n ksGPT -c conda-forge python=3.12 -y

# Initialize conda for shell interaction and set conda to automatically activate the base environment
RUN conda init bash \
    && echo "conda activate ksGPT" >> ~/.bashrc

# Copy the requirements.txt file into the container at /workspace
COPY requirements.txt /workspace/

# Install the Python requirements in the ksGPT environment
RUN conda run -n ksGPT pip install --no-cache-dir -r requirements.txt

# Download the SpaCy NLP model in the eAI environment
RUN conda run -n ksGPT python -m spacy download en_core_web_sm

# Set the default environment to eAI when starting the container
# This will activate the eAI environment for any interactive or non-interactive shell
ENV CONDA_DEFAULT_ENV=ksGPT
ENV CONDA_PREFIX=/opt/conda/envs/ksGPT
ENV PATH=$CONDA_PREFIX/bin:$PATH

# Ensure that the conda environment is activated on startup
ENTRYPOINT ["conda", "run", "-n", "ksGPT", "/bin/bash"]
