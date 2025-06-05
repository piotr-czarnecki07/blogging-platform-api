from django.urls import path
from . import views

urlpatterns = [
    path('getById/<int:blogid>/', views.getById),
    path('getByTitle/<str:blogtitle>/', views.getByTitle),
    path('post/', views.post),
    path('update/<int:blogid>/', views.update),
    path('delete/<int:blogid>/', views.delete),
    path('getall/', views.getall),
    path('getByTag/<str:term>/', views.getByTag)
]