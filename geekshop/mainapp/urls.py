from django.urls import path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.SpecialProductsListView.as_view(), name='products'),
    path('category/<int:pk>/', views.ProductsListView.as_view(), name='category'),
    path('product/<int:pk>/', views.ProductListView.as_view(), name='product')

]
