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

    

    # home page - these have a static part, but abstracted (hence separate category)
    (r'^$', 'vizwall.views.home'),
    (r'^home/', 'vizwall.views.home'),
    (r'^index/', 'vizwall.views.home'),    
    # news 
    (r'^news/', include('vizwall.news.urls')),
    # vizwall team
    (r'^team/', include('vizwall.accounts.urlsteam')),
    # accounts
    (r'^accounts/', include('vizwall.accounts.urls')),
    # static pages 
    (r'^facilities/', 'vizwall.planarpages.views.facilities', {'pk_id': 1}),   
    (r'^research/', 'vizwall.views.research'),
    (r'^faq/', 'vizwall.views.faq'),
    (r'^overview/', 'vizwall.views.overview'),
    (r'^contact/', 'vizwall.views.contact'),
    # end static pages

    # Events and calendar!
    (r'^calendar/', include('vizwall.events.urls_calendar')), # just calendar views
    (r'^events/', include('vizwall.events.urls')), # events views
    
    
    (r'^gallery/vizwall/', 'vizwall.views.galvizwall'),
    (r'^gallery/haptic/', 'vizwall.views.galhaptic'),
    
    
    
    #TEMPORARY
    (r'^static/', include('vizwall.planarpages.urls')),   
 
    (r'^eventrequest/', 'vizwall.views.eventrequest'),
    (r'^eventdetail/', 'vizwall.views.eventdetail'),
    (r'^adminmenu/', 'vizwall.views.adminmenu'),
    (r'^admin-accounts/', 'vizwall.views.adminaccounts'),
    (r'^admin-accounts-detail/', 'vizwall.views.adminaccountsdetail'),
    (r'^admin-news/', 'vizwall.views.adminnews'),
    (r'^admin-news-detail/', 'vizwall.views.adminnewsdetail'),
    (r'^admin-pages/', 'vizwall.views.adminpages'),
    (r'^admin-pages-detail/', 'vizwall.views.adminpagesdetail'),
    (r'^admin-event-request/', 'vizwall.views.admineventrequest'),


    # Uncomment the next line to enable the admin:
    (r'^admin/', include('vizwall.customadmin_urls')),
    
    #(r'^login/', 'vizwall.views.login_view'),
    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #(r'^logout/', 'vizwall.views.logout_view'),
    (r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    
)
