from django.contrib import admin
from django.contrib.admin import ModelAdmin

from doctor.models import Doctor, Notification


@admin.register(Doctor)
class DoctorAdmin(ModelAdmin):
    list_display = ["user", "full_name", "specialization", "qualification", "year_of_exp", "next_appointment_date"]


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ["doctor", "appointment", "status", "date", "seen"]

