from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('imageProcess', views.imageProcess, name='imageProcess')
]