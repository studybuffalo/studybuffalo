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

# Create a postgres DB for django
RUN apt-get install -y postgresql-9.5 postgresql-contrib
RUN service postgresql start
RUN sleep 10
RUN pg_lsclusters
RUN cat /var/log/postgresql/postgresql-9.5-main.log
RUN ls /var/lib/postgresql/
RUN ls /var/lib/postgresql/data
USER postgres
RUN psql --command "CREATE USER django WITH SUPERUSER PASSWORD 'django';"
RUN createdb -O django django
