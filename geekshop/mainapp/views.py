from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'title':'Главная'
    }
    return render(request, 'mainapp/index.html',context=context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)


links = [
    {
        'url': 'products',
        'title': 'все'
    },
    {
        'url': 'products_home',
        'title': 'дом'
    },
    {
        'url': 'products_office',
        'title': 'офис'
    },
    {
        'url': 'products_modern',
        'title': 'модерн'
    },
    {
        'url': 'products_classic',
        'title': 'классика'
    },
]


def products(request):
    context = {
        'list_menu': links,
        'title': 'Продукты'

    }
    return render(request, 'mainapp/products.html', context=context)


def products_home(request):
    context = {
        'list_menu': links,
        'title': 'Продукты для дома'
    }
    return render(request, 'mainapp/products.html', context=context)


def products_office(request):
    context = {
        'list_menu': links,
        'title': 'Продукты для офиса'

    }
    return render(request, 'mainapp/products.html', context=context)


def products_modern(request):
    context = {
        'list_menu': links,
        'title': 'Продукты модерн'

    }
    return render(request, 'mainapp/products.html', context=context)


def products_classic(request):
    context = {
        'list_menu': links,
        'title': 'Продукты классические'

    }
    return render(request, 'mainapp/products.html', context=context)
