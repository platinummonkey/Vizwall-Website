from django.conf.urls.defaults import *

urlpatterns = patterns('vizwall.planarpages.customadmin.views',
    (r'^$', 'index'),
    (r'^edit/(?P<page_id>\d+)/$', 'editPage'),
)
