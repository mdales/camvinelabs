from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^django/lastfm/', include('camvinelabs.lastfm.urls')),
    (r'^django/bbcbackstage/', include('camvinelabs.bbcbackstage.urls')),
)
