from django.conf.urls import include, url
import agenda.views
from django.contrib import admin
admin.autodiscover()


monthRegex = r'^year/(?P<year>[0-9]{4})/month/(?P<month>[0-9]{1,2})$'
urlpatterns = [
    url(r'^$', agenda.views.index, name='index'),
    url(r'^streak$', agenda.views.streak, name='streak'),
    url(r'^save', agenda.views.save, name='save'),
    url(monthRegex, agenda.views.month, name='month'),
    url(r'^admin/', include(admin.site.urls)),
]
