from django.urls import path

from .views import DoctorCreateView, DoctorDetailView

urlpatterns = [
    path("", DoctorCreateView.as_view(), name="doctor-create"),
    path("<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),
]
