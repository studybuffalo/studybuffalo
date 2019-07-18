
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

        base_search_url = 'https://idbl.ab.bluecross.ca/idbl/drugsList?'
        base_detail_url = 'https://idbl.ab.bluecross.ca/idbl/drugDetails?detailId='

        for ptc in PTC.objects.filter(ptc_1__isnull=True):
            # Find a drug DIN for this PTC
            drug = ptc.drugs.first()
            din = drug.din

            # Search by DIN on iDBL to get an ABC ID
            search_url = '{}searchTerm={}&dinPin={}'.format(base_search_url, din, din)
            search_response = session.get(url)

            if search_response.status_code == 200:
                search_html = BeautifulSoup(search_response.text, 'lxml')
                abc_id = 1

                # get PTC data from detail page
                detail_url = '{}{}'.format(base_detail_url, abc_id)
                detail_response = session.get(detail_url)

                if detail_response.status_code == 200:
                    detail_html = BeautifulSoup(detail_response.text, 'lxml')
                    ptc_table = detail_html.find(
                        id='theContent'
                    ).find(
                        class_='container printable'
                    ).find(
                        class_='abc-drug-detail-table'
                    ).find_all(
                        'tr', recursive=False
                    )[1].table.find_all(
                        'tr'
                    )

                    # get ID at each level and see if text can be found in PTC records
                    # If found, add this to the PTC
                    # If not, flag it for manual review

            # Sleep of 1 second to avoid hitting iDBL too often
            time.sleep(1)
