from __future__ import absolute_import

import logging

import requests
from django.db import connection
from django.db import transaction

from utility.models import StateCode

STATE_CODE_API = "https://www.whizapi.com/api/v2/util/ui/in/indian-states-list?" \
                           "project-app-key=jffeir4slhowadi13uudvvb7"


def run():
    r = requests.get(STATE_CODE_API)
    data = r.json()
    with transaction.atomic():
        StateCode.objects.filter().delete()
        for d in data['Data']:
            datum = {
                'name': d['Name'].strip().lower(),
                'type': d['Type'].strip().lower()
            }
            StateCode.objects.create(**datum)

        logging.getLogger('custom').debug('Client constants created!')
    connection.close()

run()
