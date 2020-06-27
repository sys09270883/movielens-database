from django.contrib import admin
from django.urls import path
from . import views

app_name = 'option_select'
urlpatterns = [
    path('result/', views.ResultView.as_view(), name='result')
]