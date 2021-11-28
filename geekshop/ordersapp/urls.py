from django.urls import path, re_path
from ordersapp import views

app_name = 'ordersapp'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('read/<int:pk>/', views.OrderDetailView.as_view(), name='read'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.OrderUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.OrderDeleteView.as_view(), name='delete'),
    path('cancel/forming/<int:pk>/', views.order_forming_complete, name='forming_cancel'),
    path('edit/<int:pk>/price/', views.EditOrderPrice.as_view())

]
