from django.conf.urls import url
from prm.views import PrmFormView, PrmOrderView

urlpatterns = [
    url(r'^$', PrmFormView.as_view()),
    url(r'^order/(?P<order_id>[a-zA-Z0-9-]+)/', PrmOrderView.as_view()),
]
