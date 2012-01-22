from django.conf.urls.defaults import *

# /admin/accounts/...

urlpatterns = patterns('vizwall.accounts.customadmin.views',
    (r'^$', 'index'),

    (r'^view/(?P<user_id>\d+)/$', 'view'),
    (r'assigned/(?P<user_id>\d+)/$', 'viewAssigned'),
    (r'assigned/$', 'viewAssigned'),
    # create new user
    (r'^create/$', 'createUser'),
    # edit user with profile
    (r'^edit/(?P<user_id>\d+)/$', 'editUser'),
    # delete user
    (r'delete/(?P<user_id>\d+)/$', 'deleteUser'),
    # deactivate user
    (r'deactivate/(?P<user_id>\d+)/$', 'deactivateUser'),
    (r'reactivate/(?P<user_id>\d+)/$', 'activateUser'),
)
