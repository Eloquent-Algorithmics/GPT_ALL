# Use the official Python image
FROM python:3.12

# Create a non-root user 'vscode' and give them sudo access
RUN apt-get update && apt-get install -y sudo && \
    useradd -m vscode -s /bin/bash && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode

# Set the working directory
WORKDIR /workspace

# Install utilities and upgrade pip
RUN apt-get install -y \
    curl \
    wget \
    git \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --upgrade pip

# Copy the requirements.txt file into the container at /workspace
COPY requirements.txt /workspace/

# Install the Python requirements
RUN pip install --no-cache-dir -r /workspace/requirements.txt

RUN pip install types-pytz

# Download the SpaCy NLP model
RUN python -m spacy download en_core_web_sm

# Switch to the 'vscode' user
USER vscode
