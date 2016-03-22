from django.conf.urls import url
from tekst.views import TekstFormView, TekstOrderView

urlpatterns = [
    url(r'^$', TekstFormView.as_view()),
    url(r'^order/(?P<order_id>[a-zA-Z0-9-]+)/', TekstOrderView.as_view()),
]
