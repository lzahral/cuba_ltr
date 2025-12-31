from django.urls import path, include
from .views import *

urlpatterns = [
    path("dashboard", index, name="index"),
    path("", index2, name="index2"),
    path("logout-page", logout_page.as_view(), name="logout-page"),
]
