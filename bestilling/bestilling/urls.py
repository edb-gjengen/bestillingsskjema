from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from bestilling.views import IndexView, AttachmentView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^design/', include('design.urls')),
    url(r'^tekst/', include('tekst.urls')),
    url(r'^prm/', include('prm.urls')),
    url(r'^$', IndexView.as_view()),
    url(r'^attachments/$', AttachmentView.as_view(), name='attachments'),
    url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )