from django.urls import path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.products, name='products'),
    path('category/<int:pk>/', views.products, name='category'),


]
