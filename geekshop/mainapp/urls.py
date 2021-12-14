from django.urls import path
from mainapp import views
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    path('', views.SpecialProductsListView.as_view(), name='products'),
    # path('category/<int:pk>/', cache_page(3600)(views.ProductsListView.as_view()), name='category'),
    path('category/<int:pk>/', views.ProductsListView.as_view(), name='category'),
    # path('product/<int:pk>/', cache_page(3600)(views.ProductListView.as_view()), name='product')
    path('product/<int:pk>/', views.ProductListView.as_view(), name='product'),
    path('favorite/<int:pk>/', views.add_favorite_product, name='add_favorite'),


]
