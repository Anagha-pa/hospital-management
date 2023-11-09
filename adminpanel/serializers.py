from rest_framework import serializers
from .models import Doctor,Departments
from users.models import UserAccount as User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions




class DepartmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departments
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
   
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
        last_name=validated_data['first_name'],

        email=validated_data['email'],
        password=validated_data['password'],
        department=validated_data['department'],
        experience=validated_data['experience'],
        qualification=validated_data['qualification'],
        gender=validated_data['gender'],
        phone_number=validated_data['phone_number'],

       )
        user.is_doctor = True
        user.save()
        return user
    

class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','email','is_active','gender','department','experience','qualification','is_doctor','phone_number']




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','is_active']
    
