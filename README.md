# Study Buffalo
## What You Will Find
Hello, we are the Study Buffalo! We are excited to see you taking an interest in our project.
This area is specifically the web hosting side of our projects. This website is currently 
created with the Django framework. This framework is part of our other projects, such as 
the Drug Price Calculator and the Equivalent Pharmaceutical ID projects.

## Licensing
We strive to keep our projects accessible to all. Everything here is open source under
the GNU Public License. We are always open to discussing other licensing options, so 
please contact us if this is an issue for you.

## Contact Us
You can always get a hold of us at studybuffalo@gmail.com, info@studybuffalo.com, or through 
GitHub itself.

## Setup Process for a Linode Server
Note: The following processes were written for a Ubuntu 16.04 server.

### Set up the Linode
1. Follow the linode instructions for connecting to the server via SSH as root

2. Run any server upgrades
```sh
apt-get update
apt-get upgrade
```

3. Set your server hostname
```sh
hostnamectl set-hostname EXAMPLE
```
```
EXAMPLE = your desired host name
```

4. Set your timezone
```sh
dpkg-reconfigure tzdata
```

5. Create a user for running the server and Django applications
```sh
adduser USERNAME
```
```
USERNAME = what you wish to name the user
```

6. Add user to the sudo group (if needed)
```sh
adduser USERNAME sudo
```
```
USERNAME = the user to add to the sudo group
```

7. Ensure the user has read, write, and executable access to everything in the home directory. You may need to adjust things with chown. Switch to your new user.
```sh
su USERNAME
```

8. Using your preferred tool, generate a RSA key-pair (on your LOCAL computer)

9. Create a folder and authorized_keys file to copy your public key into the file (all on one line)
```sh
mkdir ~/.ssh
nano ~/.ssh/authorized_keys
```

10. Set permission the directory and key file
```sh
sudo chmod 700 -R ~/.ssh
sudo chmod 600 ~/.ssh/authorized_keys
```

11. Logout and test that your SSH access works

12. Once the SSH is set up correctly, disallow root logins, password authentication, and set which protocol to listen on

```sh
sudo nano /etc/ssh/sshd_config
```
```
...
PermitRootLogin no
...
PasswordAuthentication no
...
AdressFamily inet # listens on IPv4
# AddressFamily inet6 # listens on IPv6
...
```

13. Restart the SSH service
```sh
sudo systemctl restart sshd
```

14. Consider setting up Fail2Ban and closing down uneeded ports on the firewall with UFW

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
    server_name WEBSITE_ADDRESS;

    access_log ACCESS_LOG_LOCATION;
    error_log ERROR_LOG_LOCATION;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root STATIC_FILE_LOCATION;
    }

    location /media/ {
        root MEDIA_FILE_LOCATION;
    }

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:LOCATION_TO_SOCKET_FILE;
    }
}
```
```
SITE_NAME: the name given to this file
WEBSITE_ADDRESS: the web address(es) for this site
ACCESS_LOG_LOCATION: where to store access logs
ERROR_LOG_LOCATION: where to store error logs
STATIC_FILE_LOCATION: the location for the django site static files
MEDIA_FILE_LOCATION: the location for the django site media files
LOCATION_TO_SOCKET_FILE: wherever was specified in the uWSGI configuration file
```
```
Note: To redirect all HTTP requests to HTTPS, change the following:
server {
    listen 80;
    listen [::]:80;
    server_name SITE_NAME;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    ssl_certificate ...
    ssl_certificate_key ...
    ...
}
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
30 3 * * 5 /usr/bin/certbot renew --quiet
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
1. Install Postfix and Dovecot (and remove Exim, if installed)
```sh
sudo apt-get install postfix
sudo apt-get install dovecot-core dovecot-imapd dovecot-pop3d
sudo apt-get remove exim4
sudo apt-get purge exim4
```

2. Make note of your SSL certificates generated above, as they will be needed in the future steps
```
Certificate => /etc/letsencrypt/live/DOMAIN.COM/fullchain.pem
Private Key => /etc/letsencrypt/live/DOMAIN.COM/privkey.pem
```

3. Configure the Postfix master.cf file by adding/uncommenting the following:
```sh
sudo nano /etc/postfix/master.cf
```
```
submission inet n       -       y       -       -       smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_wrappermode=no
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_recipient_restrictions=permit_mynetworks,permit_sasl_authenticated,reject
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
  -o milter_macro_daemon_name=ORIGINATING
  -o smtpd_sasl_type=dovecot
  -o smtpd_sasl_path=private/auth
```

4. Configure the Postfix main.cf file by adding the following (note the cert_file and key_file locations - they should match the ones you recorded above):
```
# TLS Parameters
smtpd_use_tls=yes
smtpd_tls_cert_file = /etc/letsencrypt/live/HOST_NAME.COM/fullchain.pem
smtpd_tls_key_file = /etc/letsencrypt/live/HOST_NAME.COM/privkey.pem
smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache
smtpd_tls_security_level = may
smtpd_tls_auth_only = no
smtpd_tls_CAfile = /etc/postfix/ssl/cacert.pem
smtpd_tls_loglevel = 1
smtpd_tls_received_header = yes
smtpd_tls_session_cache_timeout = 3600s
smtpd_tls_protocols = !SSLv2, !SSLv3
smtpd_sasl_local_domain =
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
smtpd_recipient_restrictions = permit_sasl_authenticated,permit_mynetworks,reject_unauth_destination
smtp_tls_security_level = may
smtp_tls_note_starttls_offer = yes
smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated defer_unauth_destination
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
tls_random_source = dev:/dev/urandom

# Hostname and user account details
myhostname = HOST_NAME.COM
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
local_recipient_maps = proxy:unix:passwd.byname $alias_maps
myorigin = /etc/mailname
mydestination = $myhostname, HOST_NAME.COM, localhost
relayhost =
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = all
inet_protocols = all
broken_sasl_auth_clients = yes

# Configuration for DKIM
milter_protocol = 2
milter_default_action = accept
smtpd_milters = inet:localhost:12301
```
```
HOST_NAME.COM = Name of your domain/server
```

5. Setup the alias config
```sh
sudo nano /etc/aliases
```
```
mailer-daemon: postmaster
postmaster: root
nobody: root
hostmaster: root
usenet: root
news: root
webmaster: root
www: root
ftp: root
abuse: root
root: USERNAME
```
```
USERNAME = user account you would like these emails to direct to
```

6. Setup the Dovecot config by replacing __the entire conents of the file__ (remember to use the proper paths for the certificate and key)
```sh
sudo nano /etc/dovecot/dovecot.conf
```
```

# Mailbox locations
mail_location = mbox:~/mail:INBOX=/var/mail/%u

# Setup IMAP and POP3
protocols = imap  pop3

disable_plaintext_auth = no
mail_privileged_group = mail
mail_location = mbox:~/mail:INBOX=/var/mail/%u

userdb {
  driver = passwd
}

passdb {
  args = %s
  driver = pam
}

service auth {
  unix_listener /var/spool/postfix/private/auth {
    group = postfix
    mode = 0660
    user = postfix
  }
}

# Set up SSL
ssl=required
ssl_cert = </etc/letsencrypt/live/DOMAIN_NAME.COM/fullchain.pem
ssl_key = </etc/letsencrypt/live/DOMAIN_NAME.COM/privkey.pem

# Enable Verbose Logging
auth_verbose = yes
auth_verbose_passwords = yes
auth_debug = yes
auth_debug_passwords = yes
mail_debug = yes
verbose_ssl = yes
```
```
DOMAIN_NAME.COM = the domain name used to register the certificate
```

7. Restart the services
```
sudo newaliases
sudo systemctl restart postfix
sudo systemctl restart dovecot
```

8. Enter an SPF record to the DNS zone
```
Name    DOMAIN.COM
Value   v=spf1 mx a mx:MAIL_DOMAIN.COM -all
```
```
DOMAIN.COM = The domain this spf applies to
MAIL_DOMAIN.COM = The mail server name, as defined in the DNS zone
```

9. Install OpenDKIM
```sh
sudo apt-get install opendkim opendkim-tools
```

10. Modify the OpenDKIM configuration file by adding the following records
```sh
sudo nano /etc/opendkim.conf
```
```
# Log to syslog
Syslog                  yes
SyslogSuccess           yes
LogWhy                  yes

# Required to use local socket with MTAs that access the socket as a non-
# privileged user (e.g. Postfix)
UMask                   002

# Set default oversign header
OversignHeaders         From

TrustAnchorFile       /usr/share/dns/root.key

AutoRestart             Yes
AutoRestartRate         10/1h

Canonicalization        relaxed/simple

ExternalIgnoreList      refile:/etc/opendkim/TrustedHosts
InternalHosts           refile:/etc/opendkim/TrustedHosts
KeyTable                refile:/etc/opendkim/KeyTable
SigningTable            refile:/etc/opendkim/SigningTable

Mode                    sv
PidFile                 /var/run/opendkim/opendkim.pid
SignatureAlgorithm      rsa-sha256

UserID                  opendkim:opendkim

Socket                  inet:12301@localhost
```

11. Connect the milter to Postfix by specifying the socket at the bottom of the file
```sh
sudo nano /etc/default/opendkim
```
```
SOCKET="inet:12301@localhost"
```

12. If not already done above, modify the Postfix main.cf file to use the milter
```sh
sudo nano /etc/postfix/main.cf
```
```
milter_protocol = 2
milter_default_action = accept
smtpd_milters = inet:localhost:12301
non_smtpd_milters = inet:localhost:12301
```

13. Create the directory structure to hold the keys
```sh
sudo mkdir /etc/opendkim
sudo mkdir /etc/opendkim/keys
```

14. Specify the trusted hosts
```sh
sudo nano /etc/opendkim/TrustedHosts
```
```
127.0.0.1
localhost
192.168.0.1/24

*.DOMAIN_NAME.COM
```
```
DOMAIN_NAME.COM = the domain name the mail server resides on
```

15. Create a key table
```sh
sudo nano /etc/opendkim/KeyTable
```
```
mail._domainkey.DOMAIN_NAME.COM DOMAIN_NAME.COM:mail:/etc/opendkim/keys/DOMAIN_NAME.COM/mail.private
```
```
DOMAIN_NAME.COM = the domain name the mail server resides on
```

16. Create a signing table
```sh
sudo nano /etc/opendkim/SigningTable
```
```
*@DOMAIN_NAME.COM mail._domainkey.DOMAIN_NAME.COM
```
```
DOMAIN_NAME.COM = the domain name the mail server resides on
```

17. Create the directories to hold the DKIM keys
```sh
cd /etc/opendkim/keys
sudo mkdir DOMAIN_NAME.COM
cd DOMAIN_NAME.COM
```
```
DOMAIN_NAME.COM = the domain name the mail server resides on
```

18. Create the keys
```sh
sudo opendkim-genkey -s mail -d DOMAIN_NAME.COM
```
```
DOMAIN_NAME.COM = the domain name the mail server resides on
```

19. Change ownership of the keys to opendkim
```sh
sudo chown opendkim:opendkim mail.private
```

20. Copy the TXT entry from the mail.txt file
```sh
sudo nano mail.txt
```
```
mail._domainkey IN TXT "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5N3lnvvrYgPCRSoqn+awTpE+iGYcKBPpo8HHbcFfCIIV10Hwo4PhCoGZSaKVHOjDm4yefKXhQjM7iKzEPuBatE7O47hAx1CJpNuIdLxhILSbEmbMxJrJAG0HZVn8z6EAoOHZNaPHmK2h4UUrjOG8zA5BHfzJf7tGwI+K619fFUwIDAQAB" ; ----- DKIM key mail for example.com
```

21. Add the DKIM record to the DNS zone (make sure it is on one line with no spaces)
```
mail._domainkey.DOMAIN.COM TXT "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5N3lnvvrYgPCRSoqn+awTpE+iGYcKBPpo8HHbcFfCIIV10Hwo4PhCoGZSaKVHOjDm4yefKXhQjM7iKzEPuBatE7O47hAx1CJpNuIdLxhILSbEmbMxJrJAG0HZVn8z6EAoOHZNaPHmK2h4UUrjOG8zA5BHfzJf7tGwI+K619fFUwIDAQAB"
```
```
DOMAIN.COM = the domain this DKIM applies to
```

22. Add a DMARC record to the DNS zone
```
Name    _dmarc.DOMAIN.COM
Value   v=DMARC1;p=none
```
```
DOMAIN.COM = the domain this DMARC applies to
```

23. Ensure a reverse lookup is present for both the ipv4 and ipv6 addresses for the linode
```
 - Login to the Linode Manager
 - Chose your linode
 - Go to the Remote Access
 - Click the Reverse DNS link under Public IPs
 - Lookup your linode server with the Target domain already listed
 - Select the IP address you want to add as a reverse lookup
```

24. Create system users without login ability to receive mail (if needed)
```
sudo adduser USERNAME --shell=/bin/false
```
```
USERNAME = the name of the user account
```
 
25. Restart all the mail systems
```sh
sudo systemctl restart postfix
sudo systemctl restart opendkim
sudo systemctl restart dovecot
```


