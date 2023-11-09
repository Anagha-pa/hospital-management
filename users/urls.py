from django.urls import path
from .views import RegisterView, RetrieveUserView,SentOTPView, OTPVerificationView, UserDetailView, UserProfileView, ProfileUpdateView, ForgotPasswordView, ResetPasswordView, ResendOTPView,AppointmentView,AppointmentHistoryView,DoctorView ,SingleDoctorView,AppointmentStatusView,AppointmentCountview

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', RetrieveUserView.as_view()),
    path('send-otp/', SentOTPView.as_view(), name='SentOTPView'),
    path('verify-otp/', OTPVerificationView.as_view(), name='otp-verification'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),  # Add the forgot password URL
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),  # Add the reset password URL
    path('appointment/', AppointmentView.as_view(), name='appointment'),
    path('appointment-count/',AppointmentCountview.as_view(),name = 'Appointment-count'),
    path('appointment/list-appointment/', AppointmentView.as_view(), name='list-appointment'),
    path('appointment/appointment-status/<int:appointment_id>/', AppointmentStatusView.as_view(), name='appointment-status'),
    path('appointment-history/', AppointmentHistoryView.as_view(), name='appointment-history'),
    path('doctor-view/', DoctorView.as_view(), name='doctor-view'),
    path('single-doctor/<int:pk>/',SingleDoctorView.as_view(), name='single-doctor'),


]

