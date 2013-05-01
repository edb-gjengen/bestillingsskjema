from django.conf.urls import patterns, include, url
from prm.views import PrmFormView, PrmOrderView

urlpatterns = patterns('tekst.views',
    (r'^$', PrmFormView.as_view()),
    (r'^order/(?P<order_id>[a-zA-Z0-9-]+)/', PrmOrderView.as_view()),
)
