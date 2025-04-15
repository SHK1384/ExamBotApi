from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.processing, name='process'),
    path('tashrihi/<int:userid>', views.add_tashrihi, name='tashrihi'),
    path('success/', views.success, name='success'),
]