FROM ubuntu:latest

# WORKDIR /bin/bash

RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN apt-get update && apt-get install -y \
    python3-distutils \
    python3-setuptools

COPY . .

RUN pip install -r requirements.txt --no-cache-dir


CMD ["python3","./scripts/app_server.py", "scripts/configuration_processing.json"]