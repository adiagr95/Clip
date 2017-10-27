from __future__ import absolute_import

import logging
from StringIO import StringIO

import pandas as pd
import requests
from django.db import connection
from django.db import transaction

from util.constants import core_const
from utility.models import ClientConstants

CLIENT_CONSTANT_FILE_URL = "https://docs.google.com/spreadsheets/d/1hhhBAKK7kCF20b_bygidlA4xBws5Jl4wi3yOw5tATeg/" \
                           "export?format=xlsx"


def run():
    r = requests.get(CLIENT_CONSTANT_FILE_URL)
    data = r.content
    xls = pd.ExcelFile(StringIO(data))

    sheet = xls.parse("CONSTANTS")
    with transaction.atomic():
        ClientConstants.objects.filter().delete()
        for index, row in sheet.iterrows():
            english_value = '' if pd.isnull(row['Value']) else row['Value']
            hindi_value = '' if pd.isnull(row['Hindi Value']) else row['Hindi Value']

            cc, created = ClientConstants.objects.get_or_create(key=row['Key'], template='')
            if created or cc.value != english_value or cc.hindi_value != hindi_value:
                cc.value = english_value
                cc.hindi_value = hindi_value
                cc.save()

    logging.getLogger('custom').debug('Client constants created!')
    connection.close()
