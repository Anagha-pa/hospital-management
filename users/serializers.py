from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserAccount,Appointment

from adminpanel.models import Departments, Doctor
from adminpanel.serializers import DoctorSerializer



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['otp_verified'] = user.otp_verified
        token['is_active'] = user.is_active
        token['is_staff'] = user.is_staff
        token['email'] = user.email
        
        # ...

        return token


class UserCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

  def validate(self, data):
    user = User(**data)
    password = data.get('password')

    try:
      validate_password(password, user)
    except exceptions.ValidationError as e:
      serializer_errors = serializers.as_serializer_error(e)
      raise exceptions.ValidationError(
        {'password': serializer_errors['non_field_errors']}
      )

    return data


  def create(self, validated_data):
    user = User.objects.create_user(
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
      email=validated_data['email'],
      password=validated_data['password'],
    )

    return user


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email',)


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)    

    def validate(self, data):
      email = data.get('email')
      otp = data.get('otp')

      if not email:
        raise serializers.ValidationError('Email is required')
      if not otp:
        raise serializers.ValidationError('OTP is required')
      return data
      

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'last_name', 'age', 'phone_number', 'address']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'first_name', 'last_name', 'age', 'address']





class AppointmentSerializer(serializers.ModelSerializer):

   
   class Meta:
      model = Appointment
      fields = '__all__'


  #  def create(self, validated_data):
  #     doctor_name = validated_data.pop('doctor')
  #     doctor = Doctor.objects.get(name=doctor_name)
  #     appointment = Appointment.objects.create(doctor=doctor, **validated_data)      
  #     appointment.save()
    
      
  #     # department = Departments.objects.filter(name = department_name)
  #     # fee = department.fee
  #     return appointment




class ListAppointments(serializers.ModelSerializer):
   class Meta:
      model = Appointment
      fields = ['first_name','last_name','age','gender','slot_date','department','doctor','fee']


class AppointmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
       model = Appointment
       fields = ['first_name','last_name','age','gender','slot_date','department','doctor','fee','payment_status']