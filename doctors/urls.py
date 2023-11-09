from django.urls import path
from .views import *



urlpatterns =[
   path('doctorlogin/',DoctorAuthenticationView.as_view()),
   path('todays-appointment/',DoctorAppointmentsView.as_view()),
    
]

