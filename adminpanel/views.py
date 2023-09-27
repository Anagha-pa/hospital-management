from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.views import View 
from .serializers import DoctorSerializer, DepartmentsSerializer
from .models import Doctor,Departments
from users.models import UserAccount,Appointment



class AdminAuthenticationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user and user.is_staff:
            return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


class AdminProfileView(APIView):
    def get(self,request):
        try:
            doctor_data = Doctor.objects.all().count()
            user_data = UserAccount.objects.all().count()
            apponitment_data = Appointment.objects.all().count()
            data = [{
                'doctor':doctor_data,
                'users':user_data,
                'apponitment':apponitment_data
            }]
            return Response(data)
        except Exception as e:
            return Response({'error':str(e)})
        



class DoctorCreateView(APIView):
    def post(self,request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":" doctor created successfully"})
        return Response(serializer.errors)
    

    def get(self,request):
        try:
            doctors = Doctor.objects.all()
            serilaizer = DoctorSerializer(doctors,many=True)
            return Response(serilaizer.data)
        except:
            return Response({"message":"doctor not found"})
        
    def get_object(self,pk):   
        try:
            return 
        
        


class DepartmentsCreateView(APIView):
    def post(self,request):

        serializer = DepartmentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Department created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self,request):
        try:
            departments = Departments.objects.all()
            serializer = DepartmentsSerializer(departments,many=True)
            return Response(serializer.data)
        except:
            return Response({'message':'Department not found'}) 



        
        






        






    
     
    
    




    
       