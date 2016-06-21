from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import agenda.views

urlpatterns = [
    url(r'^$', agenda.views.index, name='index'),
    url(r'^foo$', agenda.views.index, name='index'),
    url(r'^year/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$', agenda.views.month, name='month'),
    url(r'^admin/', include(admin.site.urls)),
]
