from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('vizwall.events.viewscalendar',
    # Example:
    # (r'^vizwall/', include('vizwall.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', 'thisMonth'),
    (r'(?P<year>\d{4})/(?P<month>\d+)/$', 'someMonth'),

    #(r'^admin/', include(admin.site.urls)),
    
)
