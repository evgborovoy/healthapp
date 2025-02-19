from django.db import models
from django.utils import timezone
from userauth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images", null=True, blank=True)
    full_name = models.CharField(max_length=90, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=60, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)  # TODO: maybe use choices
    qualification = models.CharField(max_length=50, null=True, blank=True)  # TODO: maybe use choices
    year_of_exp = models.CharField(max_length=90, null=True, blank=True)
    next_appointment_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"Doctor {self.full_name}"


class Notification(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New appointment"
        CANCEL = "CANCEL", "Cancel appointment"

    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE, null=True, blank=True,
                                    related_name="doctor_appointment_notification")
    status = models.CharField(max_length=20, choices=Status.choices)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doctor {self.doctor.full_name} - Notification({self.status})"
