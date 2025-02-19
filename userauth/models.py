from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class UserRole(models.TextChoices):
        DOCTOR = "Doctor", "Doctor"
        PATIENT = "Patient", "Patient"

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=80, null=True, blank=True)
    user_role = models.CharField(max_length=20, choices=UserRole.choices, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        email_username, _ = self.email.split("@")
        if self.username is None or self.username == "":
            self.username = email_username
        super(User, self).save(*args, **kwargs)
