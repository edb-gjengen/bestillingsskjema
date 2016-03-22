from django.conf.urls import url

from design.views import DesignFormView, DesignOrderView

urlpatterns = [
    url(r'^$', DesignFormView.as_view()),
    url(r'^order/(?P<order_id>[a-zA-Z0-9-]+)/', DesignOrderView.as_view()),
]
