# -*- coding: UTF-8 -*-
import os
import numpy as np
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError, transaction
from django.db.models import Sum
from conf import ROOT_DIR
from core.models import *
from order.models import *
from util import error_msg, core_util
from util.constants import core_const
from core.controllers import item_ctrl


def run(file_path):
    with transaction.atomic():
        response = []
        # business = Business.objects.get(id=3006)
        # contacts = business.contacts.all()
        # for contact in contacts:
        items = Item.objects.filter().order_by('name')
        for r in items:
            row = [str(r.id),
                   core_util.capitalize(r.name),
                   r.hindi,
                   core_util.capitalize(r.sub_category.name),
                   core_util.capitalize(r.sub_category.category.name),
                   core_util.capitalize(r.unit),
                   r.hsn_code,
                   r.gst_rate,
                   core_util.capitalize(r.img)]
            response.append(row)

        data = np.array(response)

        df = pd.DataFrame(data, columns=['ID', 'Item', 'Hindi', 'SubCategory', 'Category', 'Unit', 'HSN Code', "GST Rate", "IMG"])
        file_full_path = os.path.join(file_path)
        writer = pd.ExcelWriter(file_full_path)

        df.to_excel(writer, sheet_name='Summary', index=False)
        writer.save()

run(os.path.join(ROOT_DIR, 'project', 'bin', 'item_export.xlsx'))