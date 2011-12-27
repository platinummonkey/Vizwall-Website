from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^vizwall/', include('vizwall.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    

    # main admin page
    (r'^$', 'vizwall.views.adminhome'),
    # news admin
    (r'^news/', include('vizwall.news.customadmin.urls')),
    
    # vizwall team
    #(r'^accounts/', include('vizwall.accounts.customadmin.urls')),
    
    # Events and calendar!
    (r'^events/', include('vizwall.events.customadmin.urls')), # events views
    
    # Flat Pages
    (r'^static/', include('vizwall.planarpages.customadmin.urls')),

    # the django admin interface
    (r'^django/', admin.site.urls), # django admin

    #(r'^login/', 'vizwall.views.login_view'),
    #(r'^logout/', 'vizwall.views.logout_view'),
)
