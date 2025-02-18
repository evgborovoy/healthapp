from django.contrib import admin
from django.contrib.admin import ModelAdmin

from patient.models import Patient, Notification


@admin.register(Patient)
class PatientAdmin(ModelAdmin):
    list_display = ["user", "full_name", "phone", "gender", "blood_group", "dob"]


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ["patient", "appointment", "status", "date", "seen"]
