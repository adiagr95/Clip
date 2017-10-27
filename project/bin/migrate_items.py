# -*- coding: UTF-8 -*-

from StringIO import StringIO

import pandas as pd
import requests
from django.db import transaction

from core.models import Category, SubCategory, Item

CLIENT_CONSTANT_FILE_URL = "https://docs.google.com/spreadsheets/d/1hhhBAKK7kCF20b_bygidlA4xBws5Jl4wi3yOw5tATeg/" \
                           "export?format=xlsx"


def run():
    with transaction.atomic():
        r = requests.get(CLIENT_CONSTANT_FILE_URL)
        data = r.content
        xls = pd.ExcelFile(StringIO(data))

        df = xls.parse('FINAL ITEMS')
        df = df.fillna('')
        for index, row in df.iterrows():
            category_name = row['Category'].lower().strip()
            print category_name
            category_hindi_name = row['CategoryHindi'].lower().strip()
            category = Category.objects.get(name=category_name)
            category.hindi = category_hindi_name
            category.save()

            sub_category_name = row['SubCategory'].lower().strip()
            sub_category_hindi_name = row['SubCategoryHindi'].lower().strip()
            sub_category = SubCategory.objects.get(name=sub_category_name, category=category)
            sub_category.hindi = sub_category_hindi_name
            sub_category.category = category
            sub_category.save()

            new_item_name = row['Item'].lower().strip()
            print new_item_name
            if 'ID' in row and row['ID']:
                item_id = row['ID']
                if Item.objects.filter(id=item_id):
                    item = Item.objects.get(id=item_id)
                else:
                    item = Item.objects.create(name=new_item_name, sub_category=sub_category)
            else:
                item = Item.objects.create(name=new_item_name, sub_category=sub_category)

            data = {
                'img': row['IMG'],
                'name': new_item_name,
                'gst_rate': row['GST Rate'],
                'hsn_code': row['HSN Code'],
                'hindi': row['Hindi'],
                'rate': 0,
                'unit': row['Unit'].lower().strip(),
                'sub_category': sub_category
            }
            Item.objects.filter(id=item.id).update(**data)

    return True

run()
