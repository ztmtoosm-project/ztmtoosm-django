"""ProjektSuper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import include, url
from django.contrib import admin
from MySuperApp import views

urlpatterns = [
    url(r'^$', include('MySuperApp.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^line/(\S+)/$', views.view3),
    url(r'^apiline2/(\S+)/$', views.view3a),
    url(r'^apiline2/$', views.view3b),
    url(r'^stop/(\S+)/$', views.view4),
    url(r'^lst/$', views.view5),
    url(r'^apiline/(\S+)/$', views.view2)
]
