from django.contrib import admin
from django.urls import path
from . import views

app_name = 'pollEmail'
urlpatterns = [
    path('email/', views.email_view, name='sendemail'),
]