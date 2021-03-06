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
from django.conf.urls import include, url, patterns
from django.contrib import admin
from core import views
from payment_gateway import views as payment_views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.home),
    url(r'^awesome/$', views.awesome),
    url(r'^protoapi/menu/(?P<place>\w+)/$', views.menu_place),
    url(r'^protoapi/menu/(?P<place>\w+)/(?P<year>\w+)/(?P<month>\w+)/$', views.menu_place_not_booked),
    url(r'^protoapi/menu/(?P<place>\w+)/(?P<year>\w+)/(?P<month>\w+)/booked/$', views.menu_place_booked),

    url(r'^protoapi/booking/$', views.BookCBV.as_view()),

    url(r'^protoapi/payment/token/$', payment_views.generate_token),
    url(r'^protoapi/payment/pay/$', payment_views.post_payment),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT}))

