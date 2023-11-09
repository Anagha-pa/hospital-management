from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView





urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path('api/users/',include('users.urls')),
    path('api/adminpanel/',include('adminpanel.urls')),
    path('api/payments/',include('payments.urls')),
    path('api/doctors/',include('doctors.urls')),
    path('api/chats/',include('chats.urls')),
    path('admin/', admin.site.urls),

]

