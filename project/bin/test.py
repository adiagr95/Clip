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
from order.controllers import order_ctrl
from util import error_msg, core_util
from util.constants import core_const
from core.controllers import item_ctrl
from core.models import Business
from util import core_util


def run():
    # # orders = Order.objects.filter()
    # # for o in orders:
    # #     if o.business.type == core_const.BUSINESS_TYPE_SUPPLIER:
    # #         o.type = core_const.ORDER_TYPE_SALES
    # #     else:
    # #         o.type = core_const.ORDER_TYPE_PURCHASE
    # #     o.save()
    # #
    # # contacts = Contact.objects.filter()
    # # for c in contacts:
    # #     mobiles = list(ContactMobile.objects.filter(contact=c).values_list('mobile', flat=True))
    # #     emails = list(ContactEmail.objects.filter(contact=c).values_list('email', flat=True))
    # #     if mobiles:
    # #         c.mobile = mobiles[0]
    # #     if emails:
    # #         c.email = ','.join(list(emails))
    # #     c.save()
    #
    businesses = Business.objects.filter(poso_id__isnull=True)
    for business in businesses:
        user = business.users.filter()
        if user.exists():
            mobile = user[0].mobile
            business.poso_id = mobile
            business.save()
    dd = core_util.start_of_day()
    print Order.objects.filter(business__type=core_const.BUSINESS_TYPE_SUPPLIER, delivery_date=dd).count()
    print Order.objects.filter(business__type=core_const.BUSINESS_TYPE_RESTAURANT, delivery_date=dd).count()
    print Order.objects.filter(delivery_date=dd).count()
    orders = Order.objects.filter(business__type=core_const.BUSINESS_TYPE_RESTAURANT, delivery_date=dd)
    for order in orders:
        print order
        print order_ctrl.send_notification(order.placed_by, order.business, order, status='created')
run()