from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('signup/', views.signup, name='signup'),
    path('team', views.team, name='team'),
    path('team/', views.team, name='team'),
    path('coders', views.coders, name='coders'),
    path('coders/', views.coders, name='coders'),
    path('events', views.events, name='events'),
    path('events/', views.events, name='events'),
    path('updateCoders', views.updateCoders, name='updateCoders'),
    path('updateCoders/', views.updateCoders, name='updateCoders'),
]
