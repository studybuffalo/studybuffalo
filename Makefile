SHELL = /bin/sh

fixtures = study_buffalo/dictionary/fixtures/language.json \
			study_buffalo/dictionary/fixtures/dictionary_type.json \
			study_buffalo/dictionary/fixtures/dictionary_class.json \
			study_buffalo/dictionary/fixtures/word_pending.json \
			study_buffalo/dictionary/fixtures/excluded_word.json \
			study_buffalo/dictionary/fixtures/word.json \
			study_buffalo/users/fixtures/users.json \
			study_buffalo/users/fixtures/emails.json

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
