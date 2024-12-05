# Base image
FROM python:3.12-slim

# Install basic tools
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && apt-get clean

# Set working directory
WORKDIR /opt/datawarehouse


RUN useradd -m -d /home/datawarehouse -s /bin/bash datawarehouse && \
    chown -R datawarehouse:datawarehouse /opt/datawarehouse

# Upgrade pip and install project dependencies
COPY .devcontainer/requirements.txt /opt/datawarehouse/.devcontainer/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r /opt/datawarehouse/.devcontainer/requirements.txt

USER datawarehouse

# Add a dummy command to keep the container running
CMD ["tail", "-f", "/dev/null"]
