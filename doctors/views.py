from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils.timezone import now
from users.models import Appointments
from users.serializers import ListAppointments
from rest_framework.permissions import IsAuthenticated



# Create your views here.
class DoctorAuthenticationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user and user.is_staff:
            return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


class DoctorAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Assuming the request user is a doctor
            doctor = request.user

            # Get the current date and time
            current_datetime = now()

            # Get today's appointments for the doctor
            appointments = Appointments.objects.filter(doctor=doctor, slot_date__date=current_datetime.date())

            serializer = ListAppointments(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)