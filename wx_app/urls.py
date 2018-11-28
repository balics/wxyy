from django.urls import path, include
from wx_app import views

urlpatterns = [
    path('', views.wx_main, name='wx_main'),
]