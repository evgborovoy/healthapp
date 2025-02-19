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


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")

    if request.method == "POST":
        print("Post method")
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            print("form is valid")
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user_ins = User.objects.get(email=email, is_active=True)
                user_auth = authenticate(request, email=email, password=password)
                print(f"Trying to authenticate: email={email}, password={password}")
                print(f"Result of authenticate(): {user_auth}")
                if user_ins is not None:
                    print(f"User authenticated: {user_auth.email}")  # Отладка
                    login(request, user_auth)
                    messages.success(request, "You successfully logged in")
                    return redirect(request.GET.get("next", "/"))
                else:
                    messages.error(request, "Invalid email or password")
            except:
                messages.error(request, "Invalid email or password")
        return redirect(request.GET.get("next", "/"))
    else:
        print("else block")
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
