from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.processing, name='process'),
]