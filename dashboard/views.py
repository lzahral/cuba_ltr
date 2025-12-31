from django.shortcuts import render
from django.views.generic import TemplateView



class logout_page(TemplateView):
    template_name = "registration/logout.html"


def index(request):
    return render(request, "dashboard/index.html")

def index2(request):
    return render(request, "dashboard/test.html")

