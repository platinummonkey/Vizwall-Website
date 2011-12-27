from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('vizwall.planarpages.views',
    # Example:
    # (r'^vizwall/', include('vizwall.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^$', 'index'),
    (r'^facilities/$', 'displayPage', {'pk_id': 1, 'right':True}),
    (r'^faq/$', 'displayPage', {'pk_id': 2}),
    (r'^overview/$', 'displayPage', {'pk_id': 3, 'right':True}),
    (r'^research/$', 'displayPage', {'pk_id': 4}),
    #(r'^details/(?P<news_id>\d+)/$', 'newsDetail'),
    
    # Display events
    #(r'^(?P<year>\d{4})/$', 'displayYearsEvents'),
    #(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'displayMonthsEvents'),
    #(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'displayDaysEvents'),
    #(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<event_id>\d+)/$', 'displaySingleEvent'),
    #(r'^event/(?P<event_id>\d+)/$','displaySingleEvent'),
    
    # Request event
    #(r'^request/$', 'requestEvent'),
    #(r'^request/confirm/$', 'requestConfirm'),
    #(r'^request/status/(?P<event_id>\d+)/$', 'requestStatus'),

    #(r'^admin/', include(admin.site.urls)),
    
)
