from decimal import Decimal

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from base.models import Service, Appointment, Billing
from patient.models import Patient
from doctor.models import Doctor


def index_view(request: HttpRequest):
    services = Service.objects.all()
    context = {
        "services": services,
    }
    return render(request, "base/index.html", context=context)


def service_detail_view(request: HttpRequest, service_id):
    service = Service.objects.get(id=service_id)
    context = {
        "service": service,
    }
    return render(request, "base/service_detail.html", context=context)

@login_required()
def book_appointment(request: HttpRequest, service_id, doctor_id):
    print("book")
    service = Service.objects.get(id=service_id)
    doctor = Doctor.objects.get(id=doctor_id)
    patient = Patient.objects.get(user=request.user)

    if request.method == "POST":
        print("post")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        patient.full_name = full_name
        patient.email = email
        patient.phone = phone
        patient.address = address
        patient.gender = gender
        patient.dob = dob
        patient.save()

        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            service=service,
            issues=issues,
            symptoms=symptoms,
            date=doctor.next_appointment_date
        )

        billing = Billing()
        billing.appointment=appointment
        billing.patient=patient
        billing.subtotal=appointment.service.cost
        billing.tax=appointment.service.cost * Decimal(0.13)
        billing.total=billing.subtotal + billing.tax
        billing.status=Billing.Status.NOT_PAID
        billing.save()

        return redirect("base:checkout", billing.billing_id)

    context = {
        "service": service,
        "doctor": doctor,
        "patient": patient,
    }
    print("context")
    return render(request, "base/book_appointment.html", context=context)

def checkout_view(request: HttpRequest, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    context = {
        "billing": billing,
    }
    return render(request, "base/checkout.html", context=context)
