from django.urls import path
from doctor.views import dashboard_view, appointments_view, appointment_detail_view, cancel_appointment, \
    complete_appointment, activate_appointment

app_name = "doctor"

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("appointments/", appointments_view, name="appointments"),
    path("appointment/<int:appointment_id>", appointment_detail_view, name="appointment_detail"),
    path("cancel-appointment/<int:appointment_id>", cancel_appointment, name="cancel_appointment"),
    path("complete-appointment/<int:appointment_id>", complete_appointment, name="complete_appointment"),
    path("activate-appointment/<int:appointment_id>", activate_appointment, name="activate_appointment"),
]
