from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import (User)

class SellerSignUpForm(UserCreationForm):

    username = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})))
    first_name = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'})))
    last_name = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lastname'})))
    password1 = forms.CharField(max_length=20, label="Password", widget=(
        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})))
    password2 = forms.CharField(max_length=20, label="Confirm-Password", widget=(
        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})))
    email = forms.CharField(max_length=100,
                            widget=(forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user


class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})))
    first_name = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'})))
    last_name = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lastname'})))
    password1 = forms.CharField(max_length=20, label="Password", widget=(
        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})))
    password2 = forms.CharField(max_length=20, label="Confirm-Password", widget=(
        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})))
    email = forms.CharField(max_length=100,
                            widget=(forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user
