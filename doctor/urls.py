from django.urls import path
from doctor.views import dashboard_view, appointments_view, appointment_detail_view

app_name = "doctor"

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("appointments/", appointments_view, name="appointments"),
    path("appointment/<int:appointment_id>", appointment_detail_view, name="appointment_detail"),
]