from django.conf.urls.defaults import *
from monitor.views import *

urlpatterns = patterns('Alarm app',
    # Alarm app
    (r'^$', main_page),
    (r'^activities/$', activities_page),
    (r'^about/$', about_page),
    (r'^help/$', help_page),
    (r'^reports/$', reports_page),
    (r'^misc/$', misc_page),
    (r'^account/$', account_page),
    (r'^logout/$', logout_page),
)
