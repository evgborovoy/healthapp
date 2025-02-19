from django.http import HttpRequest
from django.shortcuts import render

from base.models import Service

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