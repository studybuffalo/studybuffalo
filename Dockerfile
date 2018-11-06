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

# Install postgresql
RUN apt-get install -y postgresql-9.5 postgresql-client-9.5 postgresql-contrib-9.5
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER django WITH SUPERUSER PASSWORD 'django';" && \
    createdb -O django django
RUN echo "local all all trust" >> /etc/postgresql/9.5/main/pg_hba.conf
RUN echo "host all all 0.0.0.0/0 trust" >> /etc/postgresql/9.5/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf
EXPOSE 5432
CMD ["/usr/lib/postgresql/9.5/bin/postgres", "-D", "/var/lib/postgresql/9.5/main", "-c", "config_file=/etc/postgresql/9.5/main/postgresql.conf"]
