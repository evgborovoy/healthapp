from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(f"Аутентификация: email={email}, password={password}")  # Отладка
        try:
            user = User.objects.get(email=email)
            print(f"Найден пользователь: {user}")  # Проверяем, найден ли пользователь
            if user.check_password(password):
                print("Пароль верный")  # Проверяем пароль
                return user
            print("Пароль неверный")
        except User.DoesNotExist:
            print("Пользователь не найден")
        return None
