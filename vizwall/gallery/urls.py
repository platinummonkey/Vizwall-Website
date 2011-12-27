from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('vizwall.gallery.views',
    # Example:
    # (r'^vizwall/', include('vizwall.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^haptic/$', 'haptic'),
    (r'^viswall/$', 'vizwall'),
    (r'^vizwall/$', 'vizwall'),    

    #(r'^admin/', include(admin.site.urls)),
    
)
