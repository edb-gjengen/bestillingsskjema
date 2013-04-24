from django.conf.urls import patterns, include, url
from design.views import DesignForm

urlpatterns = patterns('design.views',
    (r'^$', DesignForm.as_view()),
)
