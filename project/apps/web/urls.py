from django.conf.urls import url

from web.views import *

urlpatterns = [
    url(r'^$', base_view.home, name="base_view.home"),
]
