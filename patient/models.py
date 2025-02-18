from django.db import models
from userauth.models import User


class Patient(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images", null=True, blank=True)
    full_name = models.CharField(max_length=90, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=60, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True, blank=True)
    blood_group = models.CharField(max_length=20, null=True, blank=True)  # TODO: maybe use choices
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Patient {self.full_name}"


class Notification(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New appointment"
        CANCEL = "CANCEL", "Cancel appointment"

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE, null=True, blank=True,
                                    related_name="patient_appointment_notification")
    status = models.CharField(max_length=50, choices=Status.choices)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient {self.patient.full_name} - Notification({self.status})"
