from django.conf.urls import patterns, include, url
from views import IndexView

urlpatterns = patterns('',
    (r'^design/', include('design.urls')),
    (r'^tekst/', include('tekst.urls')),
    (r'^prm/', include('prm.urls')),
    (r'^$', IndexView.as_view())
)
