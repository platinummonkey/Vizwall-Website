from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('vizwall.accounts.viewsteam',
    # Example:
    # (r'^vizwall/', include('vizwall.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # main staff page
    (r'^$', 'vizwallTeam'),
    

    # staff page
    #(r'/(?P<staff_id>\w)/$', 'viewStaffMember'),



    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    
)
