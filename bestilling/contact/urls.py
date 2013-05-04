from django.conf.urls import patterns, include, url
from contact.views import ContactFormView

urlpatterns = patterns('contact.views',
    (r'^$', ContactFormView.as_view()),
)
