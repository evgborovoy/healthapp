from django.urls import path
from base.views import index_view, service_detail_view, book_appointment, checkout_view

app_name = "base"

urlpatterns = [
    path("", index_view, name="index"),
    path("service/<int:service_id>", service_detail_view, name="service_detail"),
    path("book-appointment/<int:service_id>/<int:doctor_id>", book_appointment, name="book_appointment"),
    path("checkout/<int:billing_id>", checkout_view, name="checkout"),
]