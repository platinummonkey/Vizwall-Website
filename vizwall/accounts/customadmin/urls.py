from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

# /admin/events/...

urlpatterns = patterns('vizwall.accounts.customadmin.views',
    # Example:
    # (r'^vizwall/', include('vizwall.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', 'index'),

    ### Approved Events ###
    # List of Events
    #(r'^active/$', 'activeEvents'),
    # Edit Event
    #(r'^active/edit/(?P<event_id>\d+)/$', 'editEvent'),
    # Delete Event
    #(r'^active/delete/(?P<event_id>\d+)/$', 'deleteEvent'),
    # De-Activate Event
    #(r'^active/deactivate/(?P<event_id>\d+)/$', 'deactivateEvent'),


    ### Requests ###
    # List Pending Events
    #(r'^requests/$', 'pendingEvents'),
    # Edit event
    #(r'^requests/edit/(?P<event_id>\d+)/$', 'editEvent'),
    # Confirm Event
    #(r'^requests/confirm/(?P<event_id>\d+)/$', 'requestConfirm'),
    # Delete Event
    #(r'^requests/delete/(?P<event_id>\d+)/$', 'deleteEvent'),
    
    
    # Display events
    ##(r'^(?P<year>\d{4})/$', 'displayYearsEvents'),
    ##(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'displayMonthsEvents'),
    #(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'displayDaysEvents'),
    ##(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<event_id>\d+)/$', 'displaySingleEvent'),
    #(r'^event/(?P<event_id>\d+)/$','displaySingleEvent'),

    #(r'^admin/', include(admin.site.urls)),
    
)
