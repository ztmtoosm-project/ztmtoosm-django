from django.conf.urls import url

from . import views
from . import views2

urlpatterns = [
    url(r'^$', views.index),
    url(r'^x/$', views.index5),
    url(r'^y/$', views2.index11),
    url(r'^api/all_lines/$', views.index2),
    url(r'^api/line_directions/(\S+)/$', views.index3),
    url(r'^api/line_stops/(\S+)/$', views.all_line_stops),
    url(r'^api/get_tree/$', views.index4a)
]
