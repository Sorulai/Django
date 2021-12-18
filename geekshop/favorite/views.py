from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, RedirectView

from favorite.models import FavoritesProducts


class FavoriteList(ListView):
    """
    Список избранных товаров
    """
    template_name = 'mainapp/favorites_user_list.html'
    model = FavoritesProducts

    def get_queryset(self):
        queryset = super().get_queryset().select_related()
        user_pk = self.request.user.pk
        if user_pk != 0:
            queryset = queryset.filter(user__pk=user_pk)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        user_pk = self.request.user.pk
        context_data['favorite_product_menu'] = FavoritesProducts.objects.filter(user__pk=user_pk).select_related()
        context_data['title'] = 'Избранные товары'
        return context_data


@login_required
def favorite_add(request, pk):
    """
    Добавление товара таблицу избранных и добавление информации в сессию, для интерактивной кноки
    :param request:
    :param pk:
    """
    if request.method == 'POST':
        if not request.session.get('favorite'):
            request.session['favorite'] = list()
        else:
            request.session['favorite'] = list(request.session['favorite'])

        item_list = next((item for item in request.session['favorite'] if item['product'] == pk), False)
        FavoritesProducts.objects.get_or_create(product_id=pk, user_id=request.user.pk)
        data = {
            'user': request.user.pk,
            'product': pk
        }
        if not item_list:
            request.session['favorite'].append(data)
            request.session.modified = True
    return HttpResponseRedirect(reverse('products:product', kwargs={'pk': pk}))


def favorite_remove(request, pk):
    """
    Удадение товара из избранных на странице продуктов и из сессии,для скрытия кнопки
    :param request:
    :param pk:
    """
    if request.method == 'POST':
        for i in request.session['favorite']:
            if i['product'] == pk and i['user'] == request.user.pk:
                i.clear()
                FavoritesProducts.objects.get(product_id=pk).delete()
        while {} in request.session['favorite']:
            request.session['favorite'].remove({})

        if not request.session['favorite']:
            del request.session['favorite']

        request.session.modified = True
        return HttpResponseRedirect(reverse('products:product', kwargs={'pk': pk}))


def favoritelist_delete(request, pk):
    """
    Удаление избранного товара на странице избранных товаров
    :param request:
    :param pk:
    """
    FavoritesProducts.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('products:favorite:favorite_list'))
