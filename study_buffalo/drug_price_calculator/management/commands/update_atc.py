
import time

from bs4 import BeautifulSoup
import requests
from sentry_sdk import capture_message
from tqdm import tqdm

from django.core.management.base import BaseCommand, CommandError

from drug_price_calculator.models import ATC


class Command(BaseCommand):
    help = 'Updates temporary ATC records with descriptions.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Create session to query the WHO ATC database
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Study Buffalo Data Extraction/2.0 (+https://studybuffalo.com/dataextraction/)',
            'From': 'studybuffalo@studybuffalo.com',
        })

        for atc in tqdm(ATC.objects.filter(atc_5__isnull=False).filter(atc_5_text__isnull=True)):
            # Assemble URL to query
            url = 'https://www.whocc.no/atc_ddd_index/?code={}'.format(atc.atc_5)

            # If valid response, can extract data
            response = session.get(url)

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')

                try:
                    # Extract ATC description
                    atc_text = soup.find(id='content').ul.table.find_all(
                        'tr', recursive=False,
                    )[1].find_all(
                        'td'
                    )[1].a.text.strip()

                    # Update the ATC record
                    atc.atc_5_text = atc_text
                    atc.save()
                except AttributeError:
                    # Unable to find data, send message for manual follow-up
                    message = 'No ATC found for {} (reference DIN: {})'.format(
                        atc.atc_5, atc.drugs.last().din
                    )
                    capture_message(message, level=20)

            # Sleep of 10 seconds to comply with robots.txt
            time.sleep(10)
