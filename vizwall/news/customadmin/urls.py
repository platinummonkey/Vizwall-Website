from django.conf.urls.defaults import *

# /admin/news/...

urlpatterns = patterns('vizwall.news.customadmin.views',

    (r'^$', 'index'),
    (r'^create/$', 'newNews'),

    # Edit News
    (r'^edit/(?P<news_id>\d+)/$', 'editNews'),
    # Delete News
    (r'^delete/(?P<news_id>\d+)/$', 'deleteNews'),
    # UnPublish News
    (r'^unpublish/(?P<news_id>\d+)/$', 'unpublishNews'),
    # Publish News
    (r'^publish/(?P<news_id>\d+)/$', 'publishNews'),
)
