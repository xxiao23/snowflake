from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^query/', views.query, name="query"),
    url(r'^ajax_get/', views.ajax_get, name="ajax_get"),
    url(r'^ajax_query/', views.ajax_query, name="ajax_query"),
    url(r'^ajax_describe/', views.ajax_describe, name="ajax_describe"),
    url(r'^login/$',auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="registration/logout.html"), name='logout'),
    url(r'^admin/', admin.site.urls),
]