from django.urls import path
from .views import RegisterView, RetrieveUserView, OTPVerificationView, UserDetailView, UserProfileView, ProfileUpdateView, ForgotPasswordView, ResetPasswordView, ResendOTPView,AppointmentView,AppointmentHistoryView 

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', RetrieveUserView.as_view()),
    path('verify-otp/', OTPVerificationView.as_view(), name='otp-verification'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),  # Add the forgot password URL
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),  # Add the reset password URL
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('appointment/', AppointmentView.as_view(), name='appointment'),
    # path('appointment/list-appointment', AppointmentView.as_view(), name='list-appointment'),
    path('appointment-history/', AppointmentHistoryView.as_view(), name='appointment-history'),


]
