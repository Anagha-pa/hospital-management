from rest_framework import serializers
from .models import Doctor,Departments



class DepartmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departments
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Doctor
        fields = '__all__'


    
