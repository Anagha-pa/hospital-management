from django.urls import path
from .views import *



urlpatterns =[
    path('adminlogin/',AdminAuthenticationView.as_view()),
    path('adminprofile/',AdminProfileView.as_view()),
    path('doctors/',DoctorCreateView.as_view(), name='create-list-doctors'),
    path('departments/',DepartmentsCreateView.as_view(), name='departments'),
    
    
]





