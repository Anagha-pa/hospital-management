from django.shortcuts import render
import json
import environ
import razorpay
from rest_framework.response import Response
from rest_framework.views import APIView


env = environ.Env()
environ.Env.read_env()

class StartPaymentView(APIView):
    def post(self,request):
        pass






