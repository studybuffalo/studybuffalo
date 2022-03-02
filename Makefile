SHELL = /bin/sh

#fixtures =

# Update a development environment
development:
	pipenv uninstall --all
	pipenv install --dev --ignore-pipfile
	pipenv run python manage.py collectstatic --noinput --settings=config.settings.development
	pipenv run python manage.py migrate --settings=config.settings.development

# Update a production environment
production:
	pipenv uninstall --all
	pipenv install --ignore-pipfile
	pipenv run python manage.py collectstatic --noinput --settings=config.settings.production
	pipenv run python manage.py migrate --settings=config.settings.production
	sudo systemctl restart uwsgi

# Install a fresh deployment environment (WILL RESET ENTIRE DATABASE)
development-fresh:
	pipenv uninstall --all
	pipenv install --dev --ignore-pipfile
	pipenv run python manage.py collectstatic --noinput --settings=config.settings.development
	pipenv run python manage.py reset_db --noinput --settings=config.settings.development
	pipenv run python manage.py migrate --settings=config.settings.development
	pipenv run python manage.py loaddata $(fixtures) --settings=config.settings.development
