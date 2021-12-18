from django.urls import path
from favorite import views

app_name = 'favorite'

urlpatterns = [
    path('', views.FavoriteList.as_view(), name='favorite_list'),
    path('add/<int:pk>/', views.favorite_add, name='add_favorite'),
    path('delete/<int:pk>', views.favorite_remove, name='remove_favorite'),
    path('deleteFavorite/<int:pk>', views.favoritelist_delete, name='delete_favorite')
]
