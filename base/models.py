from django.db import models
from django.db.models import TextChoices, ForeignKey
from shortuuid.django_fields import ShortUUIDField
from patient.models import Patient
from doctor.models import Doctor


class Service(models.Model):
    image = models.FileField(upload_to="images", null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.ManyToManyField(Doctor, blank=True)

    def __str__(self):
        return f"{self.name} - {self.cost}"


class Appointment(models.Model):
    class Status(TextChoices):
        PLANNED = "PLANNED", "Planned"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"
        CONSIDERED = "CONSIDERED", "Considered"

    appointment_id = ShortUUIDField(length=6, max_length=10, unique=True, alphabet="1234567890")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="service_appointment")
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="doctor_appointment")
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="patient_appointment")
    date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONSIDERED)

    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.full_name}"


class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Medical record for {self.appointment.patient.full_name}, doctor - {self.appointment.doctor.full_name}"


class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    test_name = models.CharField(max_length=100, null=True, blank=True)
    test_result = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.test_name


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medication = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.full_name}"


class Billing(models.Model):
    class Status(TextChoices):
        PAID = "PAID", "Paid"
        NOT_PAID = "NOT_PAID", "Not paid"

    billing_id = ShortUUIDField(length=6, max_length=10, unique=True, alphabet="1234567890")
    patient = ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="patient_billing")
    appointment = ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True,
                             related_name="appointment_billing")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_PAID)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Bill #{self.id} for {self.patient}, total: {self.total}"
