from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

# /admin/events/...

urlpatterns = patterns('vizwall.events.customadmin.views',
    # Example:
    # (r'^vizwall/', include('vizwall.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', 'index'),


    ### Approved Events ###
    # List of Events
    (r'^active/$', 'activeEvents'),
    # Add new Event
    (r'^active/add/$', 'newEvent', {'redirectURL':'/admin/events/active/'}),
    # Edit Event
    (r'^active/edit/(?P<event_id>\d+)/$', 'editEvent', {'redirectURL':'/admin/events/active/'}),
    # Delete Event
    (r'^active/delete/(?P<event_id>\d+)/$', 'deleteEvent', {'redirectURL':'/admin/events/active/'}),
    # De-Activate Event
    (r'^active/deactivate/(?P<event_id>\d+)/$', 'deactivateEvent', {'redirectURL':'/admin/events/active/'}),


    ### Requests ###
    # List Pending Events
    (r'^requests/$', 'pendingEvents'),
    # redirects 'pending' to 'requests'
    (r'^pending/$', lambda x: HttpResponseRedirect('/admin/events/requests/')),
    # Add new event
    (r'^requests/add/$', 'newEvent', {'redirectURL':'/admin/events/requests/'}),
    # Edit event
    (r'^requests/edit/(?P<event_id>\d+)/$', 'editEvent', {'redirectURL':'/admin/events/requests/'}),
    # Publish Event
    (r'^requests/publish/(?P<event_id>\d+)/$', 'requestConfirm', {'redirectURL':'/admin/events/requests/'}),
    # Delete Event
    (r'^requests/delete/(?P<event_id>\d+)/$', 'deleteEvent', {'redirectURL':'/admin/events/requests/'}),
    # Decline Event
    (r'^requests/decline/(?P<event_id>\d+)/$', 'declineEvent', {'redirectURL':'/admin/events/requests/'}),
    
    ## Declined Events ##
    # List of Declined Events
    (r'^declined/$', 'declinedEvents'),
    # Oops, undo decline
    (r'^declined/undodecline/(?P<event_id>\d+)/$', 'undoDecline'),
    # Delete Event
    (r'^declined/delete/(?P<event_id>\d+)/$', 'deleteEvent', {'redirectURL':'/admin/events/declined/'}),
    # Edit Event
    (r'^declined/edit/(?P<event_id>\d+)/$', 'editEvent', {'redirectURL':'/admin/events/declined/'}),
    # Publish Event
    (r'^declined/publish/(?P<event_id>\d+)/$', 'requestConfirm', {'redirectURL':'/admin/events/declined/'}),

    ## Reports ##
    # Report Home Page # contains form for generation
    (r'^reports/$', 'reportsIndex'),
    # Generate Report 
    (r'^reports/generate/csv/$', 'reportsIndex', {'download': 'csv'}),
    # 

 
    # Display events
    ##(r'^(?P<year>\d{4})/$', 'displayYearsEvents'),
    ##(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'displayMonthsEvents'),
    #(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'displayDaysEvents'),
    ##(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<event_id>\d+)/$', 'displaySingleEvent'),
    #(r'^event/(?P<event_id>\d+)/$','displaySingleEvent'),

    #(r'^admin/', include(admin.site.urls)),
    
)
