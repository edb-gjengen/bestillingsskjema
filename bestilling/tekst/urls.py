from django.conf.urls import patterns, include, url
from tekst.views import TekstFormView, TekstOrderView

urlpatterns = patterns('tekst.views',
    (r'^$', TekstFormView.as_view()),
    (r'^order/(?P<order_id>[a-zA-Z0-9-]+)/', TekstOrderView.as_view()),
)
