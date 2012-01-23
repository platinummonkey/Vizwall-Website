from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler403 = 'vizwall.planarpages.views.error_403'
handler404 = 'vizwall.planarpages.views.error_404'
handler500 = 'vizwall.planarpages.views.error_500'

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
    (r'^facilities/', 'vizwall.planarpages.views.displayPage', {'pk_id': 1, 'right':True}),
    (r'^research/', 'vizwall.planarpages.views.displayPage', {'pk_id': 4}),
    (r'^faq/', 'vizwall.planarpages.views.displayPage',{'pk_id': 2}),
    (r'^overview/', 'vizwall.planarpages.views.displayPage', {'pk_id': 3,'right': True}),
    # end static pages
    # contact
    (r'^contact/', 'vizwall.views.contact'),

    # Events and calendar!
    (r'^calendar/', include('vizwall.events.urls_calendar')), # just calendar views
    (r'^events/', include('vizwall.events.urls')), # events views
    
    
    (r'^gallery/vizwall/', 'vizwall.views.galvizwall'),
    (r'^gallery/haptic/', 'vizwall.views.galhaptic'),
    
    (r'^captcha/', include('captcha.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include('vizwall.customadmin_urls')),
    
    #(r'^login/', 'vizwall.views.login_view'),
    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #(r'^logout/', 'vizwall.views.logout_view'),
    (r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    
)
