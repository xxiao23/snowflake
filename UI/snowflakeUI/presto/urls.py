from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^query/', views.query, name="query"),
    url(r'^ajax_get/', views.ajax_get, name="ajax_get"),
]