from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from bestilling.views import IndexView, AttachmentView
from design import urls as design_urls
from tekst import urls as tekst_urls
from prm import urls as prm_urls

admin.autodiscover()

urlpatterns = [
    url(r'^design/', include(design_urls)),
    url(r'^tekst/', include(tekst_urls)),
    url(r'^prm/', include(prm_urls)),
    url(r'^$', IndexView.as_view()),
    url(r'^attachments/$', AttachmentView.as_view(), name='attachments'),
    url(r'^admin/', include(admin.site.urls)),
]
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
