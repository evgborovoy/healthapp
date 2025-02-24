from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from patient.models import Patient
from doctor.models import Doctor

from userauth.forms import UserLoginForm, UserRegisterForm
from userauth.models import User


def logout_view(request: HttpRequest):
    logout(request)
    messages.success(request, "You have successfully logged out of your account")
    return redirect("/")


def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, "Вы уже вошли в аккаунт")
        return redirect("/")

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user_instance = User.objects.get(email=email, is_active=True)
            except User.DoesNotExist:
                messages.error(request, "Пользователь с таким email не найден")
                return redirect("userauth:sign_in")

            user_authenticate = authenticate(request, email=email, password=password)

            if user_authenticate is not None:
                login(request, user_authenticate)
                messages.success(request, "Вы успешно вошли в систему")
                return redirect("/")
            else:
                messages.error(request, "Неверный email или пароль")
                return redirect("userauth:sign_in")

        else:
            print("Ошибки формы:", form.errors)  # Вывод ошибок в консоль
            messages.error(request, f"Ошибка в форме: {form.errors}")  # Вывод ошибок в интерфейсе

    else:
        form = UserLoginForm()

    return render(request, "userauth/sign_in.html", {"form": form})


def register_view(request: HttpRequest):
    if request.user.is_authenticated:
        messages.success(request, "You already logged in")
        # TODO: redirect to main page
        return redirect("/")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            user_role = form.cleaned_data["user_role"]
            user.set_password(password1)  # Хешируем пароль
            user.save()  # Сохраняем пользователя в БД

            # Создаем профиль в зависимости от роли пользователя
            if user_role == User.UserRole.DOCTOR:
                Doctor.objects.create(user=user, full_name=full_name)
            else:
                Patient.objects.create(user=user, full_name=full_name)

            # Аутентифицируем пользователя
            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, "Account successfully created")
            # TODO: redirect to main page
            return redirect("/")
        else:
            messages.error(request, "Registration failed. Check the entered data.")
    else:
        form = UserRegisterForm()
    context = {
        "form": form,
    }
    return render(request, "userauth/sign_up.html", context=context)
