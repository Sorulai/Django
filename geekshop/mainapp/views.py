from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mainapp.service_currency import get_currency
from mainapp.models import Product, ProductCategory
from mainapp.serializers import ProductSerializer
from mainapp.services import get_hot_product, get_same_products


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'categories'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True).select_related()
            cache.set(key, links_menu)
        return links_menu
    return ProductCategory.objects.filter(is_active=True).select_related()


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category_item = cache.get(key)
        if category_item is None:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category_item)
        return category_item
    return get_object_or_404(ProductCategory, pk=pk)


# def index(request):
#     context = {
#         'title': 'Главная',
#         'products': Product.objects.all()[:4],
#     }
#     return render(request, 'mainapp/index.html', context=context)


class Index(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        is_home = Q(category__name='Дом')
        is_office = Q(category__name='Офис')
        context['products'] = Product.objects.filter(
            is_home | is_office
        )
        context['currency'] = get_currency()
        return context


# def contact(request):
#     context = {
#         'title': 'Контакты',
#     }
#     return render(request, 'mainapp/contact.html', context=context)


class Contacts(TemplateView):
    template_name = 'mainapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context


class ProductsListView(ListView):
    template_name = 'mainapp/products_list.html'
    model = Product
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset().select_related()
        category_pk = self.kwargs.get('pk')
        if category_pk != 0:
            queryset = queryset.filter(Q(category__pk=category_pk))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs.get('pk')
        context_data['list_menu'] = ProductCategory.objects.filter(Q(is_active=True)).select_related()
        context_data['title'] = 'Продукты'
        if category_pk == 0:
            context_data['category'] = {
                'name': 'Все',
                'pk': 0
            }
        else:
            context_data['category'] = get_object_or_404(ProductCategory, pk=category_pk)
        return context_data


# def products(request, pk=None, page=1):
#     links_menu = ProductCategory.objects.all()
#     if pk is not None:
#         if pk == 0:
#             products_list = Product.objects.all()
#             category_item = {
#                 'name': 'Все',
#                 'pk': 0
#             }
#         else:
#             category_item = get_object_or_404(ProductCategory, pk=pk)
#             products_list = Product.objects.filter(category__pk=pk)
#
#         paginator = Paginator(products_list, 2)
#         try:
#             products_paginator = paginator.page(page)
#         except PageNotAnInteger:
#             products_paginator = paginator.page(1)
#         except EmptyPage:
#             products_paginator = paginator.page(paginator.num_pages)
#
#         context = {
#             'list_menu': links_menu,
#             'title': 'Продукты',
#             'products': products_paginator,
#             'category': category_item,
#         }
#         return render(request, 'mainapp/products_list.html', context=context)
#     hot_product = get_hot_product()
#     same_products = get_same_products(hot_product)
#
#     context = {
#         'list_menu': links_menu,
#         'title': 'Продукты',
#         'hot_product': hot_product,
#         'same_products': same_products,
#     }
#     return render(request, 'mainapp/products.html', context=context)

class SpecialProductsListView(ListView):
    template_name = 'mainapp/products.html'
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Продукты'
        context_data['list_menu'] = ProductCategory.objects.filter(Q(is_active=True)).select_related()
        context_data['hot_product'] = get_hot_product()
        context_data['same_products'] = get_same_products(context_data['hot_product'])
        return context_data


# def product(request, pk):
#     links_menu = ProductCategory.objects.all()
#     context = {
#         'product': get_object_or_404(Product, pk=pk),
#         'links_menu': links_menu
#
#     }
#     return render(request, 'mainapp/product.html', context=context)


class ProductListView(ListView):
    template_name = 'mainapp/product.html'
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_pk = self.kwargs.get('pk')
        context_data['list_menu'] = ProductCategory.objects.filter(Q(is_active=True)).select_related()
        context_data['product'] = get_object_or_404(Product, pk=product_pk)
        return context_data


@api_view(['POST'])
def load_products(request):
    """
    Сохранение данных в таблицу product
    :param request:
    :return:
    """
    if request.method == 'POST':
        print(request)
        if request.headers.get('Authorization') == settings.AUTH_HEADER:
            for product in request.data:
                product_serializer = ProductSerializer(data=product)
                if product_serializer.is_valid():
                    product_serializer.save()
                    return Response(product_serializer.data, status=status.HTTP_201_CREATED)
                return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
