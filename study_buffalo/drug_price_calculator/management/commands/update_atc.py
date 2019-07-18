
import time

from bs4 import BeautifulSoup
import requests

from django.core.management.base import BaseCommand, CommandError

from drug_price_calculator.models import ATC


class Command(BaseCommand):
    help = 'Updates temporary ATC records with descriptions.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Study Buffalo Data Extraction/2.0 (+https://studybuffalo.com/dataextraction/)',
            'From': 'studybuffalo@studybuffalo.com',
        })

        base_url = 'https://www.whocc.no/atc_ddd_index/?code='

        for atc in ATC.objects.filter(atc_5__isnull=False).filter(atc_5_text__isnull=True):
            url = '{}{}'.format(base_url, atc.atc_5)
            self.stdout.write('Extracting data for {}'.format(atc.atc_5))

            response = session.get(url)

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')

                try:
                    atc_text = soup.find(id='content').ul.table.find_all(
                        'tr', recursive=False,
                    )[1].find_all(
                        'td'
                    )[1].a.text.strip()

                    self.stdout.write('Extracted "{}"'.format(atc_text))

                    atc.atc_5_text = atc_text
                    atc.save()
                except AttributeError:
                    self.stdout.write(
                        'No code found for {} (reference DIN: {})'.format(
                            atc.atc_5, atc.drugs.last().din
                        )
                    )

            # Sleep of 10 seconds to comply with robots.txt
            time.sleep(10)
