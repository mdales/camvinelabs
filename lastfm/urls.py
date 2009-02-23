from django.conf.urls.defaults import *

# rendering for the main page
urlpatterns = patterns(
    'lastfm.views',
    (r'^weekly/', 'weekly'),
    )
