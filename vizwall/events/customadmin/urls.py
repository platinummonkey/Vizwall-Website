from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect

# /admin/events/...

urlpatterns = patterns('vizwall.events.customadmin.views',
    (r'^$', 'index'),

    #### Generic View ###
    (r'^edit/(?P<event_id>\d+)/$', 'editEvent', {'redirectURL':'/admin/events/'}),
    (r'^delete/(?P<event_id>\d+)/$', 'deleteEvent', {'redirectURL':'/admin/events/'}),
    (r'^publish/(?P<event_id>\d+)/$', 'requestConfirm', {'redirectURL':'/admin/events/'}),
    (r'^deactivate/(?P<event_id>\d+)/$', 'deactivateEvent', {'redirectURL':'/admin/events/'}),
    #### end Generic Views ###


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
    (r'^requests/confirm/(?P<event_id>\d+)/$', 'requestConfirm', {'redirectURL':'/admin/events/requests/'}),
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
)
