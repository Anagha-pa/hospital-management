from django.shortcuts import render
import json
import environ
import razorpay
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer
from django.conf import settings

env = environ.Env()
environ.Env.read_env()


class StartPaymentView(APIView):
    def post(self, request):
        print("ddfd")
        amount = request.data['amount']
        final_amount = int(float(amount) * 100)
        name = request.data['name']
        print(amount)
        print(settings.PUBLIC_KEY)
        print(env('SECRET_KEY'))


        client = razorpay.Client(auth=(settings.PUBLIC_KEY, settings.SECRET_KEY))

        payment = client.order.create({"amount": final_amount,
                                       "currency": "INR",
                                       "payment_capture": 1})
        print(payment)

        order = Order.objects.create(
            order_product=name, order_amount=final_amount, order_payment_id=payment["id"])
        serializer = OrderSerializer(order)
        data = {
            "payment": payment,
            "order": serializer.data
        }
        return Response(data)


class HandlePaymentSuccess(APIView):
    def post(self, request):
        res = json.loads(request.data.get("response"))

        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        for key in res.keys():
            if key == 'razorpay_order_id':
                ord_id = res[key]
            elif key == 'razorpay_payment_id':
                raz_pay_id = res[key]
            elif key == 'razorpay_signature':
                raz_signature = res[key]

        order = Order.objects.get(order_payment_id=ord_id)

        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }

        client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

        # checking if the transaction is valid or not by passing above data dictionary in
        # razorpay client if it is "valid" then check will return None

        check = client.utility.verify_payment_signature(data)

        if check is not None:
            print("Redirect to error url or error page")
            return Response({'error': 'Something went wrong'})

        order.isPaid = True
        order.save()

        res_data = {
            'message': 'payment successfully received!'
        }
        return Response(res_data)


