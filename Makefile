SHELL = /bin/sh
THIS_FILE := $(lastword $(MAKEFILE_LIST))
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
			study_buffalo/hc_dpd/fixtures/dpd.json \
			study_buffalo/hc_dpd/fixtures/original_active_ingredient.json \
			study_buffalo/hc_dpd/fixtures/original_biosimilar.json \
			study_buffalo/hc_dpd/fixtures/original_company.json \
			study_buffalo/hc_dpd/fixtures/original_drug_product.json \
			study_buffalo/hc_dpd/fixtures/original_form.json \
			study_buffalo/hc_dpd/fixtures/original_inactive_product.json \
			study_buffalo/hc_dpd/fixtures/original_packaging.json \
			study_buffalo/hc_dpd/fixtures/original_pharmaceutical_standard.json \
			study_buffalo/hc_dpd/fixtures/original_route.json \
			study_buffalo/hc_dpd/fixtures/original_schedule.json \
			study_buffalo/hc_dpd/fixtures/original_status.json \
			study_buffalo/hc_dpd/fixtures/original_therapeutic_class.json \
			study_buffalo/hc_dpd/fixtures/original_veterinary_species.json \
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
			study_buffalo/updates/fixtures/update.json \
			study_buffalo/users/fixtures/users.json \
			study_buffalo/users/fixtures/emails.json

.PHONY: install-django-fixtures install-development \
		install-development-fresh install-development-fixtures \
		install-production

# Prompt to require confirmation before proceeding with Make target
confirm-install:
	@echo -n "This will clear all Django content. Enter 'yes' to proceed [yes/no]. " && read ans && [ $${ans:-N} = yes ]

# Install fixtures and associated files for development server
# NOTE: MAY OVERWRITE EXISTING DATABASE AND MEDIA CONTENT
install-django-fixtures:
	mkdir -p study_buffalo/media/play/audio
	mkdir -p study_buffalo/media/play/images/original
	mkdir -p study_buffalo/media/play/images/resized
	mkdir -p study_buffalo/media/publications
	mkdir -p study_buffalo/media/study_guides
	mkdir -p study_buffalo/media/home/update
	cp study_buffalo/media/fixtures/test_audio.mp3 study_buffalo/media/play/audio
	cp study_buffalo/media/fixtures/test_image.png study_buffalo/media/play/images/original
	cp study_buffalo/media/fixtures/test_image.png study_buffalo/media/play/images/resized
	cp study_buffalo/media/fixtures/test_document.pdf study_buffalo/media/publications
	cp study_buffalo/media/fixtures/test_document.pdf study_buffalo/media/study_guides
	cp study_buffalo/media/fixtures/test_image.png study_buffalo/media/home/update
	cp study_buffalo/media/fixtures/test_icon.png study_buffalo/media/home/update
	pipenv run python manage.py loaddata $(fixtures) --settings=config.settings.development

# Install/update a development environment
install-development:
	pipenv uninstall --all
	pipenv install --dev --ignore-pipfile
	pipenv run python manage.py collectstatic --noinput --settings=config.settings.development
	pipenv run python manage.py migrate --settings=config.settings.development

# Install a fresh development envrionment without any fixtures
# NOTE: WILL RESET ENTIRE DATABASE
install-development-fresh: confirm-install
	pipenv uninstall --all
	pipenv install --dev --ignore-pipfile
	pipenv run python manage.py reset_db --noinput --settings=config.settings.development
	rm -rf staticfiles/*
	find study_buffalo/media/ -mindepth 1 -not -path "*/fixtures" -not -path "*/fixtures/*"  -delete
	pipenv run python manage.py collectstatic --noinput --settings=config.settings.development
	pipenv run python manage.py migrate --settings=config.settings.development

# Install a fresh development environment with fixtures
# NOTE: WILL RESET ENTIRE DATABASE
install-development-fixtures: confirm-install
	pipenv uninstall --all
	pipenv install --dev --ignore-pipfile
	pipenv run python manage.py reset_db --noinput --settings=config.settings.development
	rm -rf staticfiles/*
	find study_buffalo/media/ -mindepth 1 -not -path "*/fixtures" -not -path "*/fixtures/*"  -delete
	pipenv run python manage.py collectstatic --noinput --settings=config.settings.development
	pipenv run python manage.py migrate --settings=config.settings.development
	$(MAKE) -f $(THIS_FILE) install-django-fixtures

# Install/update a production environment
install-production:
	pipenv uninstall --all
	pipenv install --ignore-pipfile
	pipenv run python manage.py collectstatic --noinput --settings=config.settings.production
	pipenv run python manage.py migrate --settings=config.settings.production
	sudo systemctl restart uwsgi
