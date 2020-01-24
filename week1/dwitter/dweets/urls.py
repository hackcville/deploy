from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('api/post', views.post),
    path('api/dweets', views.dweets),

]
