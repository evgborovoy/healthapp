from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages

from base import models as base_models
from base.models import Appointment
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


@login_required
def cancel_appointment(request: HttpRequest, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = Appointment.Status.CANCELLED
    appointment.save()
    messages.success(request, "Прием отменен")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def complete_appointment(request: HttpRequest, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = Appointment.Status.COMPLETED
    appointment.save()
    messages.success(request, "Прием завершен")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def activate_appointment(request: HttpRequest, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = Appointment.Status.PLANNED
    appointment.save()
    messages.success(request, "Прием возобновлен")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def add_medical_record(request: HttpRequest, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        base_models.MedicalRecord.objects.create(appointment=appointment, diagnosis=diagnosis, treatment=treatment)
        messages.success(request, "Медицинская запись добавлена")
        return redirect("doctor:appointment_detail", appointment.appointment_id)

@login_required
def update_medical_record(request: HttpRequest, appointment_id, medical_record_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_record = base_models.MedicalRecord.objects.get(id=medical_record_id, appointment=appointment)
    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        medical_record.diagnosis = diagnosis
        medical_record.treatment = treatment
        medical_record.save()
        messages.success(request, "Медицинская запись обновлена")
        return redirect("doctor:appointment_detail", appointment.appointment_id)

