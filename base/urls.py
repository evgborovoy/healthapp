from django.urls import path
from base.views import index_view, service_detail_view

app_name = "base"

urlpatterns = [
    path("", index_view, name="index"),
    path("service/<int:service_id>", service_detail_view, name="service_detail"),
]