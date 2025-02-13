# Use wolfi-base as the base image
FROM cgr.dev/chainguard/wolfi-base AS image

# All intermediate files during first-stage build are stored under /setup
# This directory is removed before second-stage build (i.e. copying runtime files to an empty image)
WORKDIR /setup



# Install necessary packages
RUN apk add --no-cache python3 
RUN apk add --no-cache python3-dev 
RUN apk add --no-cache py3-pip 


# Create necessary directories
RUN mkdir -p /etc/apk/keyrings /etc/apk/sources.list.d


# Configure sudo for passwordless execution
RUN echo "ALL ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Create ssh directory for root
RUN mkdir -m 0700 /root/.ssh



# Python setup
WORKDIR /setup/python
RUN apk update && apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip

# Some Python packages expect certain dependencies to already be installed
COPY pypi-packages.txt ./ 
RUN pip install --require-hashes --requirement pypi-packages.txt



# Remove setup files
RUN rm -rf /setup

# Second stage build
FROM scratch
COPY --from=image / /
WORKDIR /app



# Test stuff
RUN  python3 --version && pip --version 

# Add analysis scripts
WORKDIR /usr/local/bin/

COPY analyze_wolfi_apk.py .

RUN chmod 755  analyze_wolfi_apk.py

# Ensure that this the last WORKDIR statement, otherwise things like cargo will break
WORKDIR /app

# Set main cmd to 'sleep 30m'
ENTRYPOINT [ "sleep" ]
CMD [ "30m" ]
