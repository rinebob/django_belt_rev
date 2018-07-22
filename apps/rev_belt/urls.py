from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^welcome$', views.welcome),
    url(r'^book/$', views.books),
    url(r'^book/(?P<id>\d+)$', views.book),
    url(r'^addbook$', views.addbook),
    url(r'^addreview/(?P<id>\d+)$', views.addreview),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^logout$', views.logout),
]