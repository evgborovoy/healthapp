from django.urls import path

from patient.views import dashboard, appointments, appointment_detail, activate_appointment, cancel_appointment, \
    profile, notifications, mark_as_seen_notification

app_name = "patient"

urlpatterns = [
    path("", dashboard, name="dashboard"),

    path("appointments/", appointments, name="appointments"),
    path("appointments/<int:appointment_id>", appointment_detail, name="appointment_detail"),
    path("appointments/<int:appointment_id>", activate_appointment, name="activate_appointment"),
    path("appointments/<int:appointment_id>", cancel_appointment, name="cancel_appointment"),

    path("profile/", profile, name="profile"),

    path("notifications/", notifications, name="notifications"),
    path("notifications/<int:notification_id>/", mark_as_seen_notification, name="mark_as_seen_notification"),

]
