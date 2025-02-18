from django.contrib import admin
from django.contrib.admin import ModelAdmin

from base.models import Service, Appointment, MedicalRecord, LabTest, Prescription, Billing


class MedicalRecordInline(admin.TabularInline):
    model = MedicalRecord


class LabTestInline(admin.TabularInline):
    model = LabTest


class PrescriptionInline(admin.TabularInline):
    model = Prescription


class BillingInline(admin.TabularInline):
    model = Billing


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ["name", "cost"]
    search_fields = ["name", "description"]
    filter_horizontal = ["available"]


@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = ["patient", "doctor", "date", "status"]
    search_fields = ["patient__user__username", "doctor__user__username"]
    # inlines используется для возможности редактирования записей моделей не переходя в них
    inlines = [MedicalRecordInline, LabTestInline, PrescriptionInline, BillingInline]


@admin.register(MedicalRecord)
class MedicalRecordAdmin(ModelAdmin):
    list_display = ["appointment", "diagnosis", "treatment"]


@admin.register(LabTest)
class LabTestAdmin(ModelAdmin):
    list_display = ["appointment", "description", "test_name", "test_result"]


@admin.register(Prescription)
class PrescriptionAdmin(ModelAdmin):
    list_display = ["appointment", "medication"]


@admin.register(Billing)
class BillingAdmin(ModelAdmin):
    list_display = ["patient", "total", "status", "date"]
