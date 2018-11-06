FROM ubuntu:16.04

RUN apt-get update
RUN apt-get upgrade -y

# Set required locale environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Get the require python version, pip, and pipenv
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.6 python3-pip
RUN pip3 install pipenv

# Create a postgres DB for django
RUN apt-get install -y postgresql-9.5 postgresql-contrib
RUN pg_createcluster 9.5 main --start
RUN /etc/init.d/postgresql start
RUN sleep 10
RUN pg_lsclusters
USER postgres
RUN psql --command "CREATE USER django WITH SUPERUSER PASSWORD 'django';"
RUN createdb -O django django
