FROM ubuntu:16.04

RUN apt-get update && \
    apt-get upgrade -y

# Set required locale environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Get the require python version, pip, and pipenv
RUN apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.6 python3-pip && \
    pip3 install pipenv
