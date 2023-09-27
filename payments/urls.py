from django.urls import path

from .views import *

urlpatterns = [
    path('pay/', StartPaymentView.as_view()),
    # path('payment/success/', HandlePaymentSuccess.as_view())
]