# Base image
FROM python:3.12-slim

# Install basic tools and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    vim \
    && apt-get clean

# Set working directory
WORKDIR /opt

# Add and configure a non-root user
RUN useradd -m -d /home/datawarehouse -s /bin/bash datawarehouse && \
    chown -R datawarehouse:datawarehouse /opt /usr

# Upgrade pip and install project dependencies
COPY .devcontainer/requirements.txt /opt/.devcontainer/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r /opt/.devcontainer/requirements.txt

# Switch to non-root user
USER datawarehouse

# Add a dummy command to keep the container running
CMD ["tail", "-f", "/dev/null"]
