from __future__ import absolute_import

import logging
from StringIO import StringIO
from django.core.exceptions import ObjectDoesNotExist
import json
import pandas as pd
import requests
from django.db import connection
from django.db import transaction

from core.models import Template

CLIENT_CONSTANT_FILE_URL = "https://docs.google.com/spreadsheets/d/1hhhBAKK7kCF20b_bygidlA4xBws5Jl4wi3yOw5tATeg/" \
                           "export?format=xlsx"


def get_boolean(value):
    if value == 'ON':
        return True
    else:
        return False


def run():
    r = requests.get(CLIENT_CONSTANT_FILE_URL)
    data = r.content
    xls = pd.ExcelFile(StringIO(data))

    sheet = xls.parse("NEW_TEMP_1")
    with transaction.atomic():
        data = [{'template_id': "T"+str(i+1)} for i in range(8)]
        first_row = 1
        for index, row in sheet.iterrows():
            if first_row:
                first_row = 0
                for i1, datum in enumerate(data):
                    datum['name'] = row['T'+str(i1 + 1)].lower().strip()
            else:
                for i2, datum in enumerate(data):
                    datum[row['ID']] = get_boolean(row['T'+str(i2 + 1)])

        for datum in data:
            try:
                template = Template.objects.get(template_id=datum['template_id'])
            except ObjectDoesNotExist:
                template = Template.objects.create(template_id=datum['template_id'], name=datum['name'])
            Template.objects.filter(id=template.id).update(name=datum['name'], data=json.dumps(datum))

    logging.getLogger('custom').debug('Templates synced!')
    connection.close()