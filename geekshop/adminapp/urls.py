from django.urls import path
from adminapp import views

app_name = 'adminapp'
urlpatterns = [
    path('users/create/', views.UsersCreateView.as_view(), name='user_create'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/update/<int:pk>', views.UsersUpdateList.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', views.UsersDeleteList.as_view(), name='user_delete'),

    path('categories/create', views.CategoryCreateView.as_view(), name='categories_create'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/update/<int:pk>/', views.CategoryUpdateList.as_view(), name='categories_update'),
    path('categories/delete/<int:pk>/', views.CategoryDeleteList.as_view(), name='categories_delete'),

    path('products/create/<int:pk>', views.ProductsCreateView.as_view(), name='products_create'),
    path('products/<int:pk>/', views.ProductsListView.as_view(), name='product_list'),
    path('products/update/<int:pk>/', views.ProductUpdateList.as_view(), name='products_update'),
    path('products/delete/<int:pk>/', views.ProductDeleteList.as_view(), name='products_delete'),
    path('products/detail/<int:pk>/', views.ProductDetailList.as_view(), name='products_detail'),

]
