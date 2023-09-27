from rest_framework import serializers;
from users.models import Appointment



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        feilds = []