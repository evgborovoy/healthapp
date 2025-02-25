from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models

from base import models as base_models
from patient.models import Patient, Notification


@login_required
def dashboard(request: HttpRequest):
    patient = Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = Notification.objects.filter(patient=patient)
    total_spent = base_models.Billing.objects.filter(patient=patient).aggregate(total_spent=models.Sum("total"))[
        "total_spent"]

    context = {
        "appointments": appointments,
        "notifications": notifications,
        "total_spent": total_spent,
    }
    return render(request, "patient/dashboard.html", context=context)


@login_required
def appointments(request: HttpRequest):
    patient = Patient.objects.get(user=request.user)
    appointments_list = base_models.Appointment.objects.filter(patient=patient)
    context = {
        "appointments": appointments_list,
    }
    return render(request, "patient/appointments.html", context=context)


@login_required
def appointment_detail(request: HttpRequest, appointment_id: int):
    patient = Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    medical_record = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescription = base_models.Prescription.objects.filter(appointment=appointment)
    context = {
        "appointment": appointment,
        "medical_record": medical_record,
        "lab_tests": lab_tests,
        "prescription": prescription,
    }
    return render(request, "patient/appointment_details.html", context=context)


@login_required
def activate_appointment(request: HttpRequest, appointment_id: int):
    patient = Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    appointment.status = base_models.Appointment.Status.PLANNED
    appointment.save()
    messages.success(request, "Запись к врачу отменена")
    return redirect("patient:appointment_detail")


@login_required
def cancel_appointment(request: HttpRequest, appointment_id: int):
    patient = Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    appointment.status = base_models.Appointment.Status.CANCELLED
    appointment.save()
    messages.success(request, "Запись к врачу отменена")
    return redirect("patient:appointment_detail")


@login_required
def notifications(request: HttpRequest):
    patient = Patient.objects.get(user=request.user)
    notifications_list = Notification.objects.filter(patient=patient, seen=False)
    seen_notifications = Notification.objects.filter(patient=patient, seen=True)
    context = {
        "not_seen_notifications": notifications_list,
        "seen_notifications": seen_notifications,
    }
    return render(request, "patient/notifications.html", context=context)


@login_required
def mark_as_seen_notification(request, notification_id):
    patient = Patient.objects.get(user=request.user)
    notification = Notification.objects.get(id=notification_id, patient=patient)
    notification.seen = True
    notification.save()
    messages.success(request, "Уведомление прочитано")
    return redirect("patient:notifications")


@login_required
def profile(request):
    patient = Patient.objects.get(user=request.user)
    if patient.dob:
        formatted_dob = patient.dob.strftime("%Y-%m-%d")
    else:
        formatted_dob = "Не назначено"  # Можно поставить дефолтное значение

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        image = request.FILES.get("image")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        blood_group = request.POST.get("blood_group")
        dob = request.POST.get("dob")

        if dob:
            patient.dob = dob
        else:
            patient.dob = None
        patient.full_name = full_name
        patient.phone = phone
        patient.address = address
        patient.gender = gender
        patient.blood_group = blood_group

        if image is not None:
            patient.image = image

        patient.save()
        messages.success(request, "Данные обновлены")
        return redirect("patient:profile")

    context = {
        "patient": patient,
        "formatted_dob": formatted_dob,
    }
    return render(request, "patient/profile.html", context=context)
