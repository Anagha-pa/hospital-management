from django.urls import path

from .views import *

urlpatterns = [
    path('pay/', StartPaymentView.as_view(),name="payment"),
    path('payment/success/', HandlePaymentSuccess.as_view(),name="payment_sucess"),
]