from django.urls import path
from doctor.views import dashboard_view, appointments_view, appointment_detail_view, cancel_appointment, \
    complete_appointment, activate_appointment, add_medical_record, update_medical_record

app_name = "doctor"

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("appointments/", appointments_view, name="appointments"),
    path("appointment/<int:appointment_id>/", appointment_detail_view, name="appointment_detail"),
    path("cancel-appointment/<int:appointment_id>/", cancel_appointment, name="cancel_appointment"),
    path("complete-appointment/<int:appointment_id>/", complete_appointment, name="complete_appointment"),
    path("activate-appointment/<int:appointment_id>/", activate_appointment, name="activate_appointment"),
    path("add-medical-record/<int:appointment_id>/", add_medical_record, name="add_medical_record"),
    path("update-medical-record/<int:appointment_id>/<int:medical_record_id>/", update_medical_record, name="update_medical_record"),
]
