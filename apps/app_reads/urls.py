from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.home),
    url(r'^books/add$', views.add_book),
    url(r'^books/(?P<num>\d+)$', views.bookInfo),
    url(r'^users/(?P<num>\d+)$', views.userInfo),
    url(r'^addBook', views.create_book),
    url(r'^logout$', views.logout),
]