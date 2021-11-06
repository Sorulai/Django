from django.urls import path
from adminapp import views

app_name = 'adminapp'
urlpatterns = [
    path('users/create/', views.user_create, name='user_create'),
    path('users/', views.users, name='user_list'),
    path('users/update/<int:pk>', views.user_update, name='user_update'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),

    path('categories/create', views.categories_create, name='categories_create'),
    path('categories/', views.categories, name='category_list'),
    path('categories/update/<int:pk>/', views.categories_update, name='categories_update'),
    path('categories/delete/<int:pk>/', views.categories_delete, name='categories_delete'),

    path('products/create/<int:pk>', views.products_create, name='products_create'),
    path('products/<int:pk>/', views.products, name='product_list'),
    path('products/update/<int:pk>/', views.products_update, name='products_update'),
    path('products/delete/<int:pk>/', views.products_delete, name='products_delete'),
    path('products/detail/<int:pk>/', views.products_detail, name='products_detail'),

]
