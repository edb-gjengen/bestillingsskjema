from django.conf.urls import patterns, include, url
from design.views import DesignFormView, DesignOrderView

urlpatterns = patterns('design.views',
    (r'^$', DesignFormView.as_view()),
    (r'^order/(?P<order_id>[a-zA-Z0-9-]+)/', DesignOrderView.as_view()),
)
