from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^line/(\S+)/$', views.view3),
    url(r'^apiline2/(\S+)/$', views.view3a),
    url(r'^apiline2/$', views.view3b),
    url(r'^stop/(\S+)/$', views.stop_view),
    url(r'^lst/$', views.view5),
    url(r'^$', views.index),
    url(r'^apiline/(\S+)/$', views.view2)
]