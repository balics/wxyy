from django.urls import path, include
from wx_app import views

urlpatterns = [
    path('', views.wx_web, name='wx_web'),
    path('ht', views.wx_main, name='wx_main'),
    path('createmenu/', views.create_menu, name='creat_menu')
]
