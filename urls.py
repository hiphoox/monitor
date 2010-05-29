import os.path
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment if you want to use the Time Tracking app as the default app 
from monitor.views import main_page

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Uncomment the next line to enable the monitor:
import monitor.urls

# Path to application media directory
site_media = os.path.join( 
  os.path.dirname(__file__), 'monitor/media/monitor' 
) 

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Uncomment the next line to enable the alarm app
    (r'^monitor/', include(monitor.urls)),
    
    # Uncomment if you want to use the Time Tracking app as the default app 
    (r'^$', main_page),   

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

print (settings.DEBUG)
if settings.DEBUG:
    # Serve Static Media files during development
    urlpatterns += patterns('',
      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
          { 'document_root': site_media }),
    )
