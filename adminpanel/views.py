from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.views import View 
from .serializers import DoctorSerializer, DepartmentsSerializer , UserSerializer,DoctorListSerializer
from .models import Doctor,Departments
from users.models import UserAccount,Appointments
from django.http import Http404
from users.serializers import AppointmentSerializer
from rest_framework.permissions import IsAuthenticated



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
    permission_classes =[IsAuthenticated]
    def get(self,request):
        try:
            doctor_data = UserAccount.objects.all().count()
            user_data = UserAccount.objects.all().count()
            apponitment_data = Appointments.objects.all().count()
            data = [{
                'doctor':doctor_data,
                'users':user_data,
                'apponitment':apponitment_data
            }]
            return Response(data)
        except Exception as e:
            return Response({'error':str(e)})



class DoctorCreateView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self,request):
        
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():


            serializer.save()
        
            return Response({"message":" doctor created successfully"})
        return Response(serializer.errors)
    

    def get(self,request):
        try:
            doctors = UserAccount.objects.filter(is_doctor=True)
            serilaizer = DoctorListSerializer(doctors,many=True)
            return Response(serilaizer.data)
        except:
            return Response({"message":"doctor not found"})
        



class DoctorUpdateView(APIView): 
    permission_classes =[IsAuthenticated]            
    def get_object(self,pk):   
        try:
            return UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            return Http404 
        

    def patch(self,request,pk,foramt=None):
        userData = self.get_object(pk)
        print(userData)
        serializer = DoctorListSerializer(userData,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response({'message':'error','error':serializer.errors})
    


class DoctorAvailableView(APIView):
    permission_classes =[IsAuthenticated]
    def get_object(self,pk):   
        try:
            return UserAccount.objects.get(pk=pk)
        except:
            return Http404   

    def patch(self,request,pk):
        try:
            doctor = self.get_object(pk)
            doctor.available = not doctor.available
            doctor.save()
            return Response({"message":"Doctor availability updated successfully"})
        except Http404:
            return Response({"message":"Doctor not found"})
        


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
        
        

class UserListView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self,request):
        try:
            users = UserAccount.objects.all()
            Serializer = UserSerializer(users,many =True)
            return Response(Serializer.data)
        except:
            return Response({"message":"User dosnot exists"})
        


class UserStatusView(APIView):   
    permission_classes =[IsAuthenticated]     
    def patch(self,request, user_id):
            try:
                user = UserAccount.objects.get(id=user_id)
                user.is_active =  not user.is_active
                user.save()
                return Response({"message":"success"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



  
class ApponitmentListView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self,request):
        try:
            appointment = Appointments.objects.all().order_by("-id")
            serializer = AppointmentSerializer(appointment,many=True)
            return Response(serializer.data)
        except:
            return Response({"message":"No Appointments"})
        

class AppointmentDelete(APIView):
     permission_classes =[IsAuthenticated]
     def delete(self,request,pk,format=None):
        try:
            userData = Appointments.objects.get(pk=pk)
            userData.delete()
            return Response({'messaage':'appointment deleted'})
        except Appointments.DoesNotExist:
            return Response({'message': 'Appointment does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
 










        
        






        






    
     
    
    




    
       