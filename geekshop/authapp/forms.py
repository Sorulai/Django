from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Слишком молод')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        email_list = list(ShopUser.objects.values('email'))
        for i in email_list:
            if data == i.get('email'):
                raise forms.ValidationError('Такой эмейл уже существует')

        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        username_list = list(ShopUser.objects.values('username'))
        for i in username_list:
            if data == i.get('username'):
                raise forms.ValidationError('Такой ник уже существует')
        return data


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Слишком молод')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        email_list = list(ShopUser.objects.values('email'))
        for i in email_list:
            if data == i.get('email'):
                raise forms.ValidationError('Такой эмейл уже существует')

        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        username_list = list(ShopUser.objects.values('username'))
        for i in username_list:
            if data == i.get('username'):
                raise forms.ValidationError('Такой ник уже существует')
        return data
