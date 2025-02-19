from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "agent@mail.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "********"}))
    class Meta:
        model = User
        fields = ["email", "password"]


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "John Doe"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "agent@mail.com"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "********"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "********"}))
    user_role = forms.ChoiceField(choices=User.UserRole.choices, widget=forms.Select(attrs={"class":"form-select"}))

    class Meta:
        model = User
        fields = ["full_name", "email", "password1", "password2", "user_role"]
