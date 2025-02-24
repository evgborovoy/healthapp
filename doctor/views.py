from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from base import models as base_models
from doctor.models import Doctor, Notification


@login_required
def dashboard_view(request: HttpRequest):
    doctor = Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    notifications = Notification.objects.filter(doctor=doctor)
    context = {
        "appointments": appointments,
        "notifications": notifications,
    }
    return render(request, "doctor/dashboard.html", context=context)


@login_required
def appointments_view(request: HttpRequest):
    doctor = Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    context = {
        "appointments": appointments,
    }
    return render(request, "doctor/appointments.html", context=context)


@login_required
def appointment_detail_view(request, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_record = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)
    context = {
        "appointment": appointment,
        "medical_record": medical_record,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions,
    }
    return render(request, "doctor/appointment_detail.html", context)
