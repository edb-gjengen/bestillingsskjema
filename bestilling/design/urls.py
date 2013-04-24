from django.conf.urls import patterns, include, url

urlpatterns = patterns('design.views',
    (r'^$', 'form'),
    (r'^submit$', 'submit'),
)
