from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework import status
from .models import UserAccount,Appointments,OTP
from .serializers import UserCreateSerializer,UserSerializer,OTPVerificationSerializer,ResendOTPSerializer
from .serializers import UserProfileSerializer,ProfileUpdateSerializer,AppointmentSerializer,ListAppointments,AppointmentHistorySerializer,DoctorViewSerializer,SingleDoctorSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
import random
from adminpanel.models import Doctor
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
from django.http import HttpResponse
from datetime import date





User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)      
        if serializer.is_valid():
            user = serializer.save()
            
            # Initiate OTP verification after user registration
            # initiate_otp_verification(request, user.email)
            
            return Response({'message':'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
        
    

class RetrieveUserView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        serializer = UserSerializer(request.user)

        return Response(serializer.data,status=status.HTTP_200_OK)        


class SentOTPView(APIView):
    def post(self,request):
        email = request.data.get('email')
        if not email:
            return Response({'error':'Email is required'},status=status.HTTP_400_BAD_REQUEST)
        
        otp = str(random.randint(1000,9999))
       
        data = OTP.objects.create(email=email,otp=otp)

        send_mail(
            'OTP verification',
            f'your OTP is : {otp} ',
            'anaghaponnore2000@gmail.com',
            [email]
        )
        return Response({'message' : 'OTP sent Successfully'},status=status.HTTP_200_OK)



class OTPVerificationView(APIView):
    def post(self,request):
        email = request.data.get('email')
        user_otp = request.data.get('otp')

        try:
            stored_otp = OTP.objects.filter(email=email).first()


        # if email !=stored_email:
        #     return Response({'message':'Email Doesnot match'},status=status.HTTP_400_BAD_REQUEST) 

            print(stored_otp.otp)
            print(user_otp)
            if user_otp == stored_otp.otp:
            
                return Response({'message':'OTP verified successfully'},status=status.HTTP_200_OK)  
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)  

        except Exception as e:

        
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  





class ResendOTPView(APIView):
    def post(self,request):
        email = request.data.get('email')
        try:
            otp = str(random.randint(1000,9999))
       
            data = OTP.objects.create(email=email,otp=otp)

            send_mail(
                'OTP verification',
                f'your OTP is : {otp} ',
                'anaghaponnore2000@gmail.com',
                [email]
            )
            return Response({'message' : 'OTP sent Successfully'},status=status.HTTP_200_OK)
        
                
        except Exception as e :
            return Response({'message': str(e)})












# class OTPVerificationView(APIView):

#     def post(self,request):
#         otp_input = request.data.get('otp')
#         user = request.user
#         # print(user)
#         #retrive the stored otp from session
#         # session_key = f'otp_{user.pk}'
#         # session = SessionStore(session_key = session_key)
#         stored_otp = settings.OTP_SETTINGS.get('otp')  
#         print(stored_otp)
      


#         if (otp_input) == (stored_otp):
#             user.otp_verified = True #otp is valid,update the user otp
#             user.is_active = True
#             user.save()
#             print("success")

#             # session.delete()

#             return Response({'message':'OTP Verified Successfully.'},status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)





class UserDetailView(APIView):
   

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)



# def generate_otp():
#     return get_random_string(length=6,allowed_chars='0123456789')

# def send_otp_email(user_email, otp):
#     subject = 'OTP Verification'
#     message = f'Your OTP is : {otp}'
#     from_email = 'anaghaponnore2000@gmail.com'
#     recipient_list = ['anaghaponnore2000@gmail.com']  # Sending OTP to the user's registered email
#     send_mail(subject, message, from_email, recipient_list)


# def initiate_otp_verification(request, user_email):
#     otp = generate_otp()
#     request.session['otp'] = otp
#     request.session.save()  # Save the session data
#     print(request.session['otp'])
#     send_otp_email(user_email, otp)

# def __str__(self):
#     return self.email



class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    



class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            reset_url = reverse('reset-password',kwargs={'uidb64':uid,'token':token})
            print(f'Reset URL: {reset_url}')
            print("hii")
            reset_url = f'http://{current_site}{reset_url}'
            send_mail(
                'Reset Your Password',
                'Click the link below to reset your password.\n\n' + reset_url,
                'anaghaponnore2000@gmail.com',  
                [email],
                fail_silently=False
            )
            return JsonResponse({'bool': True,'msg':'Plesea check your email'})
        else:
            return JsonResponse({'bool': False,'msg':'Invalid email'})
       
    

class ResetPasswordView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Token is valid; let the user reset their password.
            return HttpResponse('You can now reset your password.', status=200)
        else:
            return HttpResponse('The password reset link is no longer valid.', status=400)



class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Assuming the request data contains the doctor's name in 'doctor' field
        print(request.data)
        doctor_name = request.data.get('doctor')
        user = request.user
        slot_date =request.data.get('slot_date')
        try:
            print("entered try")
            doctor = UserAccount.objects.get(first_name=doctor_name)
            print(doctor.id)
        except Exception as e:
            print(e)
       
        # Add the doctor to the request data
        # request.data['doctor'] = doctor.pk
        # request.data['user'] = user.pk

        appoinment_data = {
            'first_name': request.data["first_name"], 
            'last_name': request.data["last_name"], 
            'age': request.data["age"], 
            'gender': request.data["gender"], 
            'phone_number': request.data["phone_number"], 
            'address': request.data["address"], 
            'department': request.data["department"], 
            'doctor': 54,
            'slot_date': request.data["slot_date"], 
            'fee': request.data["fee"],
            'time': request.data["time"],
            'user': request.user.pk
        }
        

        serializer = AppointmentSerializer(data=appoinment_data)
        


        if serializer.is_valid():
            serializer.save()
            try:
                print(slot_date)
                appointment_count = Appointments.objects.filter(slot_date=slot_date).count()
                print(appointment_count)
            except:
                pass
            return Response({'message': 'Appointment booked successfully', 'count':appointment_count}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def get(self,request):
        try:
            appointments = Appointments.objects.filter(user=request.user)
            serializer = ListAppointments(appointments,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class AppointmentCountview(APIView):
        permission_classes = [IsAuthenticated]
        def get(self,request):

            slot_date = request.data.get('slot_date')
            appointment_count = Appointments.objects.filter(slot_date=slot_date).count()   
            return Response({ 'count':appointment_count}, status=status.HTTP_201_CREATED) 
        



class AppointmentStatusView(APIView):
    def patch(self,request,appointment_id):
        try:
            appointment_status = Appointments.objects.get(id=appointment_id)
            appointment_status.status =  "cancelled" 
            appointment_status.save()
            return Response({"message":"success"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)  





class UserStatusView(APIView):        
    def patch(self,request, user_id):
            try:
                user = UserAccount.objects.get(id=user_id)
                user.is_active =  not user.is_active
                user.save()
                return Response({"message":"success"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



     

class AppointmentHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            appointment_history = Appointments.objects.filter(user=request.user)
            serializer = AppointmentHistorySerializer(appointment_history,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message':'Department not found'})




class DoctorView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            doctor_view = UserAccount.objects.all()
            serializer = DoctorViewSerializer(doctor_view,many=True)
            return Response(serializer.data,status.HTTP_200_OK)
        except:
            return Response({'message':'There is no Doctor'})


class SingleDoctorView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            single_doctor = UserAccount.objects.get(pk=pk)
            serializer = SingleDoctorSerializer(single_doctor,many=False)
            return Response(serializer.data,status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({"message":"There is no doctor"})
        


        
