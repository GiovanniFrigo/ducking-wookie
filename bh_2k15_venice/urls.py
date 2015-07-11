"""bh_2k15_venice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'^protoapi/menu/(?P<place>\w+)/$', views.menu_place),
    url(r'^protoapi/menu/(?P<place>\w+)/(?P<year>\w+)/(?P<month>\w+)/$', views.menu_place_non_booked),
    url(r'^protoapi/menu/(?P<place>\w+)/(?P<year>\w+)/(?P<month>\w+)/booked/$', views.menu_place_booked),
    url(r'^admin/', include(admin.site.urls)),
]
