from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from apps.core.views import *

urlpatterns = [
    url(r'^users/signin$', signin),
    url(r'^users/signup$', signup),
    url(r'^users$', users),
    url(r'^users/(?P<pk>[0-9]+)$', user_entity),
    url(r'^users/(?P<pk>[0-9]+)/posts' , posts),
    # url(r'^users/check_auth$', check_auth),
    # url(r'^users/signin$', signin),
    # url(r'^users/forget_password$', forgot_password),
    # url(r'^users/signup$', signup),
    # url(r'^users/reset_password$', reset_password),
    # url(r'^users/confirm_otp$', confirm_otp),
    # url(r'^users/resend_otp$', resend_otp),
    #
    #
    #
    # url(r'^users/(?P<pk>[0-9]+)$', user_entity),
    # url(r'^users/(?P<pk>[0-9]+)/set_default_business$', set_default_business),
    # url(r'^users/(?P<pk>[0-9]+)/change_password$', change_password),
    #
    # url(r'^users/(?P<pk>[0-9]+)/businesses$', business_entities),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)$', business_entity),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/logo$', upload_logo),
    #
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/badges$', get_badges),
    #
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/users$', business_user_entities),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/users/(?P<uk>[0-9]+)$', business_user_entity),
    #
    #
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/send_closing_items$', send_closing_items_link),
    #
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/contacts$', contact_entities),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/contacts/(?P<ck>[0-9]+)$', contact_entity),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/contacts/search$', search_contact),
    #
    #
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/contacts/(?P<ck>[0-9]+)/items$', business_contact_item_entities),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/items$', business_item_entities),
    #
    # url(r'^users/(?P<pk>[0-9]+)/items/search$', search_item),
    # url(r'^businesses/(?P<bk>[0-9]+)/items/closing_items.pdf$', closing_items_pdf),
    #
    #
    # url(r'^users/(?P<pk>[0-9]+)/sub_categories$', sub_category_entities),
    # url(r'^users/(?P<pk>[0-9]+)/sub_categories/(?P<sk>[0-9]+)$', sub_category_entity),
    #
    #
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/contacts/(?P<ck>[0-9]+)/payments$', payment_entities),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/contacts/(?P<ck>[0-9]+)/payments/(?P<tk>[0-9]+)$', payment_entity),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/contacts/(?P<ck>[0-9]+)/payment$', payment),
    # url(r'^handle_payment$', handle_payment),
    #
    #
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/expenses/titles$', expense_title_entities),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/expenses/titles/(?P<title>[a-z]+)$', expense_entities),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/expenses/(?P<ek>[0-9]+)$', expense_entity),
    #
    #
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/supplier_requests$', supplier_request_entities),
    # url(r'^users/(?P<pk>[0-9]+)/businesses/(?P<bk>[0-9]+)/working_capitals$', working_capital_entities),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
