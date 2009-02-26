from django.conf.urls.defaults import *

# rendering for the main page
urlpatterns = patterns(
    'bbcbackstage.views',
    (r'^schedule/(\w+)/', 'schedule_now'),
    )
