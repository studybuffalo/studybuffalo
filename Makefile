SHELL = /bin/sh

fixtures = study_buffalo/dictionary/fixtures/language.json \
			study_buffalo/dictionary/fixtures/dictionary_type.json \
			study_buffalo/dictionary/fixtures/dictionary_class.json \
			study_buffalo/dictionary/fixtures/word_pending.json \
			study_buffalo/dictionary/fixtures/excluded_word.json \
			study_buffalo/dictionary/fixtures/word.json \
			study_buffalo/drug_price_calculator/fixtures/atc.json \
			study_buffalo/drug_price_calculator/fixtures/ptc.json \
			study_buffalo/drug_price_calculator/fixtures/special_authorization.json \
			study_buffalo/drug_price_calculator/fixtures/drug.json \
			study_buffalo/drug_price_calculator/fixtures/price.json \
			study_buffalo/drug_price_calculator/fixtures/clients.json \
			study_buffalo/drug_price_calculator/fixtures/coverage_criteria.json \
			study_buffalo/drug_price_calculator/fixtures/subs_bsrf.json \
			study_buffalo/drug_price_calculator/fixtures/subs_generic.json \
			study_buffalo/drug_price_calculator/fixtures/subs_manufacturer.json \
			study_buffalo/drug_price_calculator/fixtures/subs_unit.json \
			study_buffalo/drug_price_calculator/fixtures/pend_bsrf.json \
			study_buffalo/drug_price_calculator/fixtures/pend_generic.json \
			study_buffalo/drug_price_calculator/fixtures/pend_manufacturer.json \
			study_buffalo/drug_price_calculator/fixtures/pend_unit.json \
			study_buffalo/play/fixtures/category.json \
			study_buffalo/play/fixtures/play_page.json \
			study_buffalo/play/fixtures/play_image.json \
			study_buffalo/play/fixtures/play_audio.json \
			study_buffalo/rdrhc_calendar/fixtures/calendar_user.json \
			study_buffalo/rdrhc_calendar/fixtures/stat_holiday.json \
			study_buffalo/rdrhc_calendar/fixtures/shift_code.json \
			study_buffalo/rdrhc_calendar/fixtures/missing_shift_code.json \
			study_buffalo/rdrhc_calendar/fixtures/shift.json \
			study_buffalo/read/fixtures/html_publication.json \
			study_buffalo/read/fixtures/document_publication.json \
			study_buffalo/read/fixtures/publication.json \
			study_buffalo/study/fixtures/html_guide.json \
			study_buffalo/study/fixtures/document_guide.json \
			study_buffalo/study/fixtures/guide.json \
			study_buffalo/substitutions/fixtures/apps.json \
			study_buffalo/substitutions/fixtures/model_fields.json \
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

# Install a fresh development environment (WILL RESET ENTIRE DATABASE)
development-fresh:
	pipenv uninstall --all
	pipenv install --dev --ignore-pipfile
	pipenv run python manage.py collectstatic --noinput --settings=config.settings.development
	pipenv run python manage.py reset_db --noinput --settings=config.settings.development
	pipenv run python manage.py migrate --settings=config.settings.development
	mkdir -p study_buffalo/media/play/audio
	mkdir -p study_buffalo/media/play/images/original
	mkdir -p study_buffalo/media/play/images/resized
	mkdir -p study_buffalo/media/publications
	mkdir -p study_buffalo/media/study_guides
	cp study_buffalo/media/fixtures/test_audio.mp3 study_buffalo/media/play/audio
	cp study_buffalo/media/fixtures/test_image.png study_buffalo/media/play/images/original
	cp study_buffalo/media/fixtures/test_image.png study_buffalo/media/play/images/resized
	cp study_buffalo/media/fixtures/test_document.pdf study_buffalo/media/publications
	cp study_buffalo/media/fixtures/test_document.pdf study_buffalo/media/study_guides
	pipenv run python manage.py loaddata $(fixtures) --settings=config.settings.development

# Install fixtures to reset development environment database (WILL
# RESET ENTIRE DATABASE)
install-fixtures:
	pipenv run python manage.py reset_db --noinput --settings=config.settings.development
	pipenv run python manage.py migrate --settings=config.settings.development
	mkdir -p study_buffalo/media/play/audio
	mkdir -p study_buffalo/media/play/images/original
	mkdir -p study_buffalo/media/play/images/resized
	mkdir -p study_buffalo/media/publications
	mkdir -p study_buffalo/media/study_guides
	cp study_buffalo/media/fixtures/test_audio.mp3 study_buffalo/media/play/audio
	cp study_buffalo/media/fixtures/test_image.png study_buffalo/media/play/images/original
	cp study_buffalo/media/fixtures/test_image.png study_buffalo/media/play/images/resized
	cp study_buffalo/media/fixtures/test_document.pdf study_buffalo/media/publications
	cp study_buffalo/media/fixtures/test_document.pdf study_buffalo/media/study_guides
	pipenv run python manage.py loaddata $(fixtures) --settings=config.settings.development
