from django.conf.urls import patterns, include, url
from design.views import DesignFormView, DesignOrderView

urlpatterns = patterns('design.views',
    (r'^$', DesignFormView.as_view()),
    (r'^order/(?P<order_id>\d+)/', DesignOrderView.as_view()),
)
