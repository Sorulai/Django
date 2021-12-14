from django.db import transaction
from django.db.models import F
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from adminapp.forms import ShopUserAdminCreateForm, ShopCategoryAdminForm, ShopProductAdminForm, ShopUserAdminEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test

from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class AccessMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UsersCreateView(AccessMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminCreateForm

    def get_success_url(self):
        return reverse('adminapp:user_list')


class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'


class UsersUpdateList(AccessMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminEditForm

    def get_success_url(self):
        return reverse('adminapp:user_list')


class UsersDeleteList(AccessMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'

    def get_success_url(self):
        return reverse('adminapp:user_list')


class CategoryCreateView(AccessMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ShopCategoryAdminForm

    def get_success_url(self):
        return reverse('adminapp:category_list')


class CategoryListView(AccessMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'


class CategoryUpdateList(AccessMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ShopCategoryAdminForm

    def get_success_url(self):
        return reverse('adminapp:category_list')


class CategoryDeleteList(AccessMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'

    def get_success_url(self):
        return reverse('adminapp:category_list')


class ProductsCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ShopProductAdminForm

    def get_success_url(self):
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])

    def get_initial(self):
        initial = super(ProductsCreateView, self).get_initial()
        initial['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return initial


class ProductsListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))


class ProductUpdateList(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ShopProductAdminForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductDetailList(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'


class ProductDeleteList(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class OrderListView(AccessMixin, ListView):
    model = Order
    template_name = 'adminapp/orders.html'

    def get_queryset(self):
        return Order.objects.all().order_by('update_at').order_by('-is_active')


class OrderUpdateView(AccessMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'adminapp/order_form.html'
    success_url = reverse_lazy('adminapp:order_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.total_cost == 0:
            self.object.delete()

        if self.object.status == 'PD':
            orderitems_list = OrderItem.objects.filter(order__pk=self.object.pk).values()
            for item in orderitems_list:
                if Product.objects.get(pk=int(item['product_id'])):
                    Product.objects.get(pk=item['product_id']).add_count_sales(item['quantity'])

        return super().form_valid(form)


class OrderDetailView(AccessMixin, DetailView):
    model = Order
    template_name = 'adminapp/order_detail.html'


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('adminapp:order_list')
    template_name = 'adminapp/order_delete.html'


class ReportView(AccessMixin, ListView):
    template_name = 'adminapp/report_table.html'
    model = Product

    # def get_queryset(self):
    #     queryset = super().get_queryset().select_related()
    #     print(queryset)
    #     return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['products'] = Product.objects.all().order_by('-count_sales').select_related()
        context_data['title'] = 'Отчет по продаже'
        return context_data




# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('adminapp:user_list'))
#
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'form': user_form
#
#     }
#     return render(request, 'adminapp/user_form.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     context = {
#         'object_list': ShopUser.objects.all().order_by('-is_active')
#     }
#     return render(request, 'adminapp/users.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     current_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)
#
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('adminapp:user_list'))
#
#     else:
#         user_form = ShopUserAdminEditForm(instance=current_user)
#
#     context = {
#         'form': user_form
#
#     }
#     return render(request, 'adminapp/user_form.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     current_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         if current_user.is_active:
#             current_user.is_active = False
#         else:
#             current_user.is_active = True
#         current_user.save()
#         return HttpResponseRedirect(reverse('adminapp:user_list'))
#     context = {
#         'object': current_user
#
#     }
#     return render(request, 'adminapp/user_delete.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def categories_create(request):
#     if request.method == 'POST':
#         category_form = ShopCategoryAdminForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:category_list'))
#
#     else:
#         category_form = ShopCategoryAdminForm()
#
#     context = {
#         'form': category_form
#
#     }
#     return render(request, 'adminapp/category_form.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     context = {
#         'object_list': ProductCategory.objects.all().order_by('-is_active')
#     }
#     return render(request, 'adminapp/categories.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def categories_update(request, pk):
#     current_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category_form = ShopCategoryAdminForm(request.POST, request.FILES, instance=current_category)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:category_list'))
#
#     else:
#         category_form = ShopCategoryAdminForm(instance=current_category)
#     context = {
#         'form': category_form
#     }
#     return render(request, 'adminapp/category_form.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def categories_delete(request, pk):
#     current_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         if current_category.is_active:
#             current_category.is_active = False
#         else:
#             current_category.is_active = True
#         current_category.save()
#         return HttpResponseRedirect(reverse('adminapp:category_list'))
#
#     context = {
#         'object': current_category
#
#     }
#     return render(request, 'adminapp/category_delete.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def products_create(request, pk):
#     current_category = get_object_or_404(ProductCategory, pk=pk)
#     product = Product(category=current_category)
#     if request.method == 'POST':
#         product_form = ShopProductAdminForm(request.POST, request.FILES, instance=product)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:product_list', kwargs={'pk': pk}))
#
#     else:
#         product_form = ShopProductAdminForm(instance=product)
#
#     context = {
#         'form': product_form
#     }
#     return render(request, 'adminapp/product_form.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     context = {
#         'category': get_object_or_404(ProductCategory, pk=pk),
#         'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active')
#     }
#     return render(request, 'adminapp/products.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def products_update(request, pk):
#     current_product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         product_form = ShopProductAdminForm(request.POST, request.FILES, instance=current_product)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:product_list', kwargs={'pk': pk}))
#
#     else:
#         product_form = ShopProductAdminForm(instance=current_product)
#     context = {
#         'form': product_form
#
#     }
#     return render(request, 'adminapp/product_form.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def products_detail(request, pk):
#     current_product = get_object_or_404(Product, pk=pk)
#     context = {
#         'object': current_product
#
#     }
#     return render(request, 'adminapp/product_detail.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def products_delete(request, pk):
#     current_product = get_object_or_404(Product, pk=pk)
#     category_pk = current_product.category.pk
#     if request.method == 'POST':
#         if current_product.is_active:
#             current_product.is_active = False
#         else:
#             current_product.is_active = True
#         current_product.save()
#         return HttpResponseRedirect(reverse('adminapp:product_list', kwargs={'pk': category_pk}))
#     context = {
#         'object': current_product,
#         'pk': category_pk
#
#     }
#     return render(request, 'adminapp/product_delete.html', context=context)
