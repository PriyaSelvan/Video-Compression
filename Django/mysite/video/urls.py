from django.conf.urls import url, include
from . import views
from django.views.generic import ListView, DetailView
from video.models import Video


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^form/', views.compress, name='compress'),
]
