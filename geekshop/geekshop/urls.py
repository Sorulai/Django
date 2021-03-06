"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from mainapp import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.Index.as_view(), name='main'),
    path('contact/', views.Contacts.as_view(), name='contact'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('order/', include('ordersapp.urls', namespace='order')),
    path('', include('social_django.urls', namespace='social')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('admin/', include('adminapp.urls', namespace='adminapp')),

    path('control/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
