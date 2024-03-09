from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('consent', views.index, name='index'),
    path('post', views.post, name='post')
]