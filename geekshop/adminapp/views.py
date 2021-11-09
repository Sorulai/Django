from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

# Create your views here.
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ShopCategoryAdminForm, ShopProductAdminForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))

    else:
        user_form = ShopUserRegisterForm()

    context = {
        'form': user_form

    }
    return render(request, 'adminapp/user_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'object_list': ShopUser.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/users.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))

    else:
        user_form = ShopUserAdminEditForm(instance=current_user)

    context = {
        'form': user_form

    }
    return render(request, 'adminapp/user_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        if current_user.is_active:
            current_user.is_active = False
        else:
            current_user.is_active = True
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:user_list'))
    context = {
        'object': current_user

    }
    return render(request, 'adminapp/user_delete.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def categories_create(request):
    if request.method == 'POST':
        category_form = ShopCategoryAdminForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))

    else:
        category_form = ShopCategoryAdminForm()

    context = {
        'form': category_form

    }
    return render(request, 'adminapp/category_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'object_list': ProductCategory.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/categories.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def categories_update(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ShopCategoryAdminForm(request.POST, request.FILES, instance=current_category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))

    else:
        category_form = ShopCategoryAdminForm(instance=current_category)
    context = {
        'form': category_form
    }
    return render(request, 'adminapp/category_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def categories_delete(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        if current_category.is_active:
            current_category.is_active = False
        else:
            current_category.is_active = True
        current_category.save()
        return HttpResponseRedirect(reverse('adminapp:category_list'))

    context = {
        'object': current_category

    }
    return render(request, 'adminapp/category_delete.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def products_create(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    product = Product(category=current_category)
    if request.method == 'POST':
        product_form = ShopProductAdminForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:product_list', kwargs={'pk': pk}))

    else:
        product_form = ShopProductAdminForm(instance=product)

    context = {
        'form': product_form
    }
    return render(request, 'adminapp/product_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'category': get_object_or_404(ProductCategory, pk=pk),
        'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active')
    }
    return render(request, 'adminapp/products.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def products_update(request, pk):
    current_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_form = ShopProductAdminForm(request.POST, request.FILES, instance=current_product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:product_list', kwargs={'pk': pk}))

    else:
        product_form = ShopProductAdminForm(instance=current_product)
    context = {
        'form': product_form

    }
    return render(request, 'adminapp/product_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def products_detail(request, pk):
    current_product = get_object_or_404(Product, pk=pk)
    context = {
        'object': current_product

    }
    return render(request, 'adminapp/product_detail.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def products_delete(request, pk):
    current_product = get_object_or_404(Product, pk=pk)
    category_pk = current_product.category.pk
    if request.method == 'POST':
        if current_product.is_active:
            current_product.is_active = False
        else:
            current_product.is_active = True
        current_product.save()
        return HttpResponseRedirect(reverse('adminapp:product_list', kwargs={'pk': category_pk}))
    context = {
        'object': current_product,
        'pk': category_pk

    }
    return render(request, 'adminapp/product_delete.html', context=context)
