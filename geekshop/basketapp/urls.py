from django.urls import path
from basketapp import views

app_name = 'basketapp'
urlpatterns = [
    path('', views.basket, name='basket'),
    path('add/<int:pk>/', views.add, name='add'),
    path('remvove/<int:pk>/', views.remove, name='remove'),
]
