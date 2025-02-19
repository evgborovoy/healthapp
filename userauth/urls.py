from django.urls import path

from userauth.views import register_view, login_view, logout_view

app_name = "userauth"

urlpatterns = [
    path("sign-up/", register_view, name="sign_up"),
    path("sign-in/", login_view, name="sign_in"),
    path("logout/", logout_view, name="logout"),
]