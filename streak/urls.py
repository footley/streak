from django.conf.urls import include, url
import agenda.views
from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()


monthRegex = r'^year/(?P<year>[0-9]{4})/month/(?P<month>[0-9]{1,2})$'
urlpatterns = [
    url(r'^$', agenda.views.index, name='index'),
    url(r'^streak$', agenda.views.streak, name='streak'),
    url(r'^save', agenda.views.save, name='save'),
    url(monthRegex, agenda.views.month, name='month'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', auth_views.login,
        {'template_name': 'admin/login.html'}, name="my_login"),
]
