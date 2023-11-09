from django.urls import path
from .views import *



urlpatterns =[
    path('adminlogin/',AdminAuthenticationView.as_view()),
    path('adminprofile/',AdminProfileView.as_view()),
    path('doctors/',DoctorCreateView.as_view(), name='create-list-doctors'),
    path('departments/',DepartmentsCreateView.as_view(), name='departments'),
    path('doctor-updation/<int:pk>/',DoctorUpdateView.as_view(),name='doctor-updation'),
    path('doctor-available/<int:pk>/',DoctorAvailableView.as_view(),name='doctor-available'),
    path('userslist/',UserListView.as_view(),name='userlist'),
    path('user-status/<int:user_id>/',UserStatusView.as_view(),name='user-status'),
    path('apponitmentlist/',ApponitmentListView.as_view(),name='appointment-list'),
    path('apponitment-delete/<int:pk>/',AppointmentDelete.as_view(),name='appointment-delete'),
    
]





