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


@login_required
def add_lab_test(request: HttpRequest, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    if request.method == "POST":
        description = request.POST.get("description")
        test_name = request.POST.get("test_name")
        test_result = request.POST.get("test_result")
        base_models.LabTest.objects.create(description=description, test_name=test_name, test_result=test_result,
                                           appointment=appointment)
        messages.success(request, "Лабораторный тест добавлен")
        return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def update_lab_test(request: HttpRequest, appointment_id, lab_test_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    lab_test = base_models.LabTest.objects.get(id=lab_test_id, appointment=appointment)
    if request.method == "POST":
        description = request.POST.get("description")
        test_name = request.POST.get("test_name")
        test_result = request.POST.get("test_result")
        lab_test.description = description
        lab_test.test_name = test_name
        lab_test.test_result = test_result
        lab_test.save()
        messages.success(request, "Лабораторный тест обновлен")
        return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def add_prescription(request: HttpRequest, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    if request.method == "POST":
        medication = request.POST.get("medication")
        base_models.Prescription.objects.create(medication=medication, appointment=appointment)
        messages.success(request, "Лечение назначено")
        return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def update_prescription(request: HttpRequest, appointment_id, prescription_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    prescription = base_models.Prescription.objects.get(id=prescription_id, appointment=appointment)
    if request.method == "POST":
        medication = request.POST.get("medication")
        prescription.medication = medication
        prescription.save()
        messages.success(request, "Лечение обновлено")
        return redirect("doctor:appointment_detail", appointment.appointment_id)
