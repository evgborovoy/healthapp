from django.urls import path
from doctor.views import dashboard_view, appointments_view, appointment_detail_view, cancel_appointment, \
    complete_appointment, activate_appointment, add_medical_record, update_medical_record, add_lab_test, \
    update_lab_test, add_prescription, update_prescription

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
    path("add-lab-test/<int:appointment_id>/", add_lab_test, name="add_lab_test"),
    path("update-lab-test/<int:appointment_id>/<int:lab_test_id>/", update_lab_test, name="update_lab_test"),
    path("add-prescription/<int:appointment_id>/", add_prescription, name="add_prescription"),
    path("update-prescription/<int:appointment_id>/<int:prescription_id>/", update_prescription, name="update_prescription"),
]
