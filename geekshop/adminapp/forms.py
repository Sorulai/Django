from authapp.forms import ShopUserEditForm, ShopUserRegisterForm
from authapp.models import ShopUser
from django import forms

from mainapp.models import ProductCategory, Product


class ShopUserAdminCreateForm(ShopUserRegisterForm):
    class Meta:
        model = ShopUser
        # fields = '__all__'
        exclude = ('password',)


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ShopCategoryAdminForm(forms.ModelForm):
    discount = forms.IntegerField(label='скидка', min_value=0, max_value=90, initial=0, required=False)

    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
