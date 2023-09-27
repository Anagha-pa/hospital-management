from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework import status
from .models import UserAccount,Appointment
from .serializers import UserCreateSerializer,UserSerializer,OTPVerificationSerializer
from .serializers import UserProfileSerializer,ProfileUpdateSerializer,AppointmentSerializer,ListAppointments,AppointmentHistorySerializer
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





# class OTPVerificationView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self,request):
#         serializer =OTPVerificationSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data.get('email')
#             entered_otp = serializer.validated_data.get('otp')
#             session_otp = request.session.get('otp')
#             print(entered_otp)
#             print('session_otp', session_otp)

#             user = UserAccount.objects.get(email=email)
#             print(user)
            
#             if  session_otp == entered_otp:
#                 user = request.user
#                 user.otp_verified = True
#                 user.save()
                # token = RefreshToken.for_user(user)

                #     return Response({'access_token': str(token.access_token)}, status=status.HTTP_200_OK)
                # else:
                #     return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        #         return Response({"message":"verified"}, status=status.HTTP_200_OK)
        #     else:
        #         return Response(serializer.errors)
        # return  Response({"message":"something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    

class OTPVerificationView(APIView):

    def post(self,request):
        otp_input = request.data.get('otp')
        user = request.user
        # print(user)
        #retrive the stored otp from session
        # session_key = f'otp_{user.pk}'
        # session = SessionStore(session_key = session_key)
        stored_otp = settings.OTP_SETTINGS.get('otp')  
        print(stored_otp)
      


        if (otp_input) == (stored_otp):
            user.otp_verified = True #otp is valid,update the user otp
            user.save()
            print("success")

            # session.delete()

            return Response({'message':'OTP Verified Successfully.'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)





class UserDetailView(APIView):
   

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)



def generate_otp():
    return get_random_string(length=6,allowed_chars='0123456789')

def send_otp_email(user_email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP is : {otp}'
    from_email = 'anaghaponnore2000@gmail.com'
    recipient_list = ['anaghaponnore2000@gmail.com']  # Sending OTP to the user's registered email
    send_mail(subject, message, from_email, recipient_list)


def initiate_otp_verification(request, user_email):
    otp = generate_otp()
    request.session['otp'] = otp
    request.session.save()  # Save the session data
    print(request.session['otp'])
    send_otp_email(user_email, otp)

def __str__(self):
    return self.email



class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ForgotPasswordView(APIView):
    def get(self, request):
        email = request.get('email')
        print(email)
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        settings.OTP_SETTINGS['otp'] = otp

        # Send OTP via email
        subject = 'Your OTP for Account Verification'
        message = f'Your OTP is: {otp}'
        from_email = 'anaghaponnore2000@gmail.com'  # Replace with your email
        recipient_list = ['anaghaponnore2000@gmail.com']

        send_mail(subject, message, from_email, recipient_list)

        otp_input = request.data.get('otp')
       
        user = request.user
        # print(user)
        #retrive the stored otp from session
        # session_key = f'otp_{user.pk}'
        # session = SessionStore(session_key = session_key)
        stored_otp = settings.OTP_SETTINGS.get('otp')  
        print(stored_otp)
      


        if (otp_input) == (stored_otp):
            user.otp_verified = True #otp is valid,update the user otp
            user.save()
            print("success")

            # session.delete()

            return Response({'message':'OTP Verified Successfully.'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)




    
    # def post(self, request):
    #     print("reached")
        
    #     print(request)
    #     email = request.data.get('email')
    #     print(email)
    #     try:
    #         user = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         return Response({'message':'user with this email does not exist.'},status=status.HTTP_400_BAD_REQUEST)   


    #     uid = urlsafe_base64_encode(force_bytes(user.pk)) 
    #     token = default_token_generator.make_token(user)
    #     rest_password_link = f"{get_current_site(request).domain}/rest-password/{uid}/{token}/"

    #     subject = 'Rest Your Password'
    #     message = render_to_string('email/rest_password_email.html',{
    #         'user': user,
    #         'rest_password_link': rest_password_link,

    #     })

    #     send_mail(subject,message, 'anaghaponnore2000@gmail.com',[user.email])

    #     return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)
    


class ResetPasswordView(View):
    def get(self, request, uidb64, token):
        try:
            uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token, self.request):

            # Token is valid; let the user reset their password.
            return Response({'message': 'You can now reset your password.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'The password reset link is no longer valid.'}, status=status.HTTP_400_BAD_REQUEST)
        



class ResendOTPView(APIView):
    def post(self, request):
        user = request.user  # Assuming the user is authenticated
        
        if user.otp_verified:
            return JsonResponse({'message': 'User is already verified.'}, status=400)
            
        # Generate and send OTP (similar to the OTPVerificationView)
        otp = generate_otp()
        user.otp = otp
        user.save()
        send_otp_email(user.email, otp)
        
        return JsonResponse({'message': 'OTP resent successfully.'})




class AppointmentView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        # Assuming the request data contains the doctor's name in 'doctor' field
        doctor_name = request.data.get('doctor')
        user = request.user

        try:
            doctor = Doctor.objects.get(name=doctor_name)
        except Doctor.DoesNotExist:
            return Response({'message': 'Doctor does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the doctor to the request data
        request.data['doctor'] = doctor.pk
        request.data['user'] = user.pk

        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Appointment booked successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def get(self,request):
        try:
            appointments = Appointment.objects.filter(user=request.user)
            serializer = ListAppointments(appointments,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

      

class AppointmentHistoryView(APIView):
    def get(self,request):
        try:
            appointment_history = Appointment.objects.all()
            serializer = AppointmentHistorySerializer(appointment_history,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message':'Department not found'})
