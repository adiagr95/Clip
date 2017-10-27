# -*- coding: UTF-8 -*-
from __future__ import absolute_import

from StringIO import StringIO

import pandas as pd
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db import transaction
from django.forms.models import model_to_dict

from core.models import *
from order.models import *
from util import core_util
from util.constants import core_const

def run():
    with transaction.atomic():
        user_ids = [4002, 16, 4160, 4005]
        try:
            business = Business.objects.get(id=1)
            business.delete()
        except ObjectDoesNotExist:
            pass
        # ************* Outlets and Employees ***********

        try:
            copying_business = Business.objects.get(id=4)
        except:
            raise IntegrityError("Copying account is missing")
        data = model_to_dict(copying_business)
        del data['users']
        del data['id']
        data['business_id'] = "B00001"
        data['name'] = "Demo Restaurant"
        data['poso_id'] = '9619851835'
        data['template'] = 'advance'
        data['is_lead'] = False

        if user_ids:
            main_user = User.objects.get(id=user_ids[0])
        else:
            raise IntegrityError("Main user is missing")

        data['id'] = 1
        business = Business.objects.create(**data)

        if not copying_business or not business or not main_user or not user_ids:
            raise IntegrityError("Google sheet is invalid")

        # ************* Users ***********
        for uid in user_ids:
            BusinessUserMapping.objects.create(user=User.objects.get(id=uid), business=business)

        # ************* Contacts ***********
        print 'Contacts'
        for contact in list(copying_business.contacts.all()):
            print contact
            contact_data = model_to_dict(contact)
            del contact_data['id']
            del contact_data['order_identifier']
            del contact_data['mobile']
            del contact_data['email']
            contact_data['business'] = business
            contact_data['contact_id'] = core_util.get_next_contact_id(Contact)
            new_contact = Contact.objects.create(**contact_data)

        # ************* Invoice ***********
        print 'Invoice'
        for closing in list(copying_business.invoices.all()):
            print closing
            closing_data = model_to_dict(closing)
            del closing_data['id']
            closing_data['business'] = business
            closing_data['contact'] = business.contacts.get(name=closing.contact.name)
            closing_data['created_by'] = main_user
            closing_data['invoice_id'] = business.business_id + "-" + core_util.get_next_invoice_id(Invoice,
                                                                                                      business)
            invoice = Invoice.objects.create(**closing_data)

        # ************* Order ***********
        print 'Order'
        for order in list(copying_business.orders.all()):
            print order
            order_data = model_to_dict(order)
            del order_data['id']
            order_data['business'] = business
            order_data['order_id'] = "P"+core_util.get_next_order_id(Order)
            order_data['contact'] = business.contacts.get(name=order.contact.name)
            order_data['placed_by'] = main_user
            order_data['challan_uploaded_by'] = main_user
            order_data['received_by'] = main_user
            if order.invoice:
                order_data['invoice'] = Invoice.objects.get(business=business, date=order.invoice.date, contact=order_data['contact'])
            new_order = Order.objects.create(**order_data)

            for order_item in list(order.items.select_related('item').all()):
                order_item_data = model_to_dict(order_item)
                del order_item_data['id']
                order_item_data['order'] = new_order
                order_item_data['item'] = order_item.item
                OrderItem.objects.create(**order_item_data)

            for challan in list(order.challan_docs.all()):
                challan_data = model_to_dict(challan)
                del challan_data['id']
                challan_data['order'] = new_order
                challan_data['user'] = main_user
                ChallanDoc.objects.create(**challan_data)

        # ************* Inventory ***********
        print 'Inventory'
        for closing in list(copying_business.closings.all()):
            print closing
            closing_data = model_to_dict(closing)
            del closing_data['id']
            closing_data['business'] = business
            closing_data['uploaded_by'] = main_user
            closing_data['user'] = main_user
            new_closing = InventoryCheck.objects.create(**closing_data)

            for closing_item in list(closing.items.select_related('item').all()):
                closing_item_data = model_to_dict(closing_item)
                del closing_item_data['id']
                closing_item_data['inventory_check'] = new_closing
                closing_item_data['item'] = closing_item.item
                InventoryCheckItem.objects.create(**closing_item_data)

            for doc in list(closing.docs.all()):
                doc_data = model_to_dict(doc)
                del doc_data['id']
                doc_data['inventory_check'] = new_closing
                InventoryDoc.objects.create(**doc_data)

        # ************* Payment ***********
        print 'Payment'
        for closing in list(copying_business.payments.all()):
            print closing
            closing_data = model_to_dict(closing)
            del closing_data['id']
            closing_data['business'] = business
            closing_data['contact'] = business.contacts.get(name=closing.contact.name)
            closing_data['user'] = main_user
            Payment.objects.create(**closing_data)
