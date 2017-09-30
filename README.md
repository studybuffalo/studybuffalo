# Study Buffalo
## What You Will Find
Hello, we are the Study Buffalo! We are excited to see you taking an interest in our project.
This area is specifically the web hosting side of our projects. This website is currently 
created with the Django framework. This framework is part of our other projects, such as 
the Drug Price Calculator and the Equivalent Pharmaceutical ID projects.

## Setup Process for a Linode Server
**_WORK IN PROGRESS_**
### Set up the Linode
1. Complete all the required security protocols

2. Create a user for running the server and Django applications

3. Add user to the sudo group (if needed)

4. Ensure the user has read, write, and executable access to everything in the home directory

### Setup the pip files and virtual environment
1. Install pip
```sh
sudo apt-get update
sudo apt-get install python-pip3
```

2. Install the virtual environment files
```sh
sudo pip3 install virtualenv virtualenvwrapper
```

3. Set up the virtual environment for python3
```sh
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
```

4. Set up the other virutal environment settings
```sh
echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
```

5. There should now be a Env folder in the home directory for your urser (~)

6. Create the project virutal environment
```sh
mkvirtualenv studybuffalo
```

7. Enable the virtual environment
```sh
workon studybuffalo
```

8. Install django and any other requirements into the virtual env .
```sh
pip3 install django
pip3 install ...
```

### Download and Test the Django Site
1. Download the project files from Git
```sh
cd ~
git clone https://github.com/studybuffalo/studybuffalo.git
```

2. Collect static
```sh
python3 ~/studybuffalo/manage.py collectstatic
```
3. Load the virtual env
```sh
workon studybuffalo
```
4. Test the server 
```sh
python3 ~/studybuffalo/manage.py runserver 0.0.0.0:8080
```

5. Close the virtual environment
```sh
deactivate
```

### Download and configure the uWSGI application server
1. Install the required libraries
```sh
sudo apt-get install python-dv
```

2. Install uWSGI
```sh
sudo pip3 install uwsgi
```

3. Test that uWSGI and the django project are working properly
```sh
uwsgi --http :8080 --home /home/USER/Env/studybuffalo --chdir /home/USER/studybuffalo --wsgi-file /home/USER/studybuffalo/sb_django/wsgi.py
```
```
USER: the user which will run the Django application
```

4. Setup the uWSGI configuration file
```sh
sudo nano /etc/uwsgi/sites/SITE_NAME.ini
```
```ini
[uwsgi]
project = PROJECT_NAME
base = /home/USER_NAME

chdir = %(base)/%(project)
home = %(base)/Env/%(project)
module = %(project).wsgi:application

master = true
processes = 5

socket = %(base)/%(project)/%(project).sock
chmod-socket = 666
vacuum = true

logto = LOG_LOCATION
```
```
SITE_NAME: the name for this file (can use project name)
PROJECT_NAME: the name of the django project
USER_NAME: the user which will run the server and django applications
LOG_LOCATION: where to save any logs
```

5. Setup the systemd script to run the uWSGI Emperor Service on startup
```sh
sudo nano /etc/systemd/system/uwsgi.service
```
```service
[Unit]
Description=uWSGI Emperor service
After=syslog.target

[Service]
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

6. Refresh systemd
```sh
sudo systemctl daemon-reload
```

7. Start the systemd uWSGI script
```sh
sudo systemctl start uwsgi
```

8. Set uWSGI to start on server boot
```sh
sudo systemctl enable uwsgi
```
9. Check status on uWSGI
```sh
systemctl status uwsgi
```

### Setup and configure Nginx
1. Install Nginx
```sh
sudo apt-get install nginx
```

2. Create a server block configuration file
```sh
sudo nano /etc/nginx/sites-available/SITE_NAME
```
```
server {
    listen 80;
    server_name WEBSITE_ADDRESS.com
    access_log ACCESS_LOG_LOCATION
    error_log ERROR_LOG_LOCATION
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root STATIC_FILE_LOCATION
    }

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:LOCATION_TO_SOCKET_FILE
    }
}
```
```
SITE_NAME: the name given to this file
WEBSITE_ADDRESS: the web address(es) for this site
ACCESS_LOG_LOCATION: where to store access logs
ERROR_LOG_LOCATION: where to store error logs
STATIC_FILE_LOCATION: the location for the django site static files
LOCATION_TO_SOCKET_FILE: wherever was specified in the uWSGI configuration file
```

3. Link the configuration file to the sites-enabled folder
```sh
sudo ln -s /etc/nginx/sites-available/SITE_NAME /etc/nginx/sites-enabled
```

4. Update the Nginx configuration to make use of the Django user
```sh
sudo nano /etc/nginx/nginx.conf
user www-data -> user USER_NAME;
```
```
USER_NAME: the user which will run the Django application
```

5. Check the configuration files
```sh
sudo service nginx configtest
```

6. Restart the Nginx service to load the new configuration
```sh
sudo service nginx restart
```

7. If not already done, start uWSGI
```sh
sudo service uwsgi start
```

### Setup SSL ###
1. Ensure ports 80 and 443 are open to allow certbot verfication
```sh
sudo ufw status numbered
sudo ufw allow 80
sudo ufw allow 443
```

2. Install certbot
```sh
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx
```

3. Generate the needed certificate(s)
```sh
sudo certbot --nginx -d SITE_NAME.com -d www.SITE_NAME.com
```
```
SITE_NAME = the domain the SSL certificate will apply to
```

4. Set up the certificate for auto renewal by generating a cron job
```sh
sudo crontab -e
```
```
...
30 30 * * 5 * /usr/bin/certbot renew --quiet
...
```

5. Generate a new Diffie-Hellman paramater
```sh
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
```

6. Update the Nginx server block with the new parameter
```sh
sudo nano /etc/nginx/sites-available/BLOCK_NAME
```
```
...
ssl_dhparam /et/ssl/certs/dhparam.pem;
...
```
```
BLOCK_NAME = the name of the server block file
```

7. Confirm the configuration file was saved correctly
```sh
sudo nginx -t
```

8. Reload Nginx
```sh
sudo systemctl reload nginx
```

9. Test out the SSL certificate at [SSL Labs](https://www.ssllabs.com/ssltest/)

### Set Up the Email Server
1. See the [Exim documentation](https://help.ubuntu.com/lts/serverguide/exim4.html)

## Licensing
We strive to keep our projects accessible to all. Everything here is open source under
the GNU Public License. We are always open to discussing other licensing options, so 
please contact us if this is an issue for you.

## Contact Us
You can always get a hold of us at studybuffalo@gmail.com, info@studybuffalo.com, or through 
GitHub itself.
