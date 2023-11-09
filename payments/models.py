from django.db import models
from users.models import Appointments,UserAccount

# Create your models here.

class Order(models.Model):
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=100)
    order_payment_id = models.CharField(max_length=100) 
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE,null = True ,blank=True)
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.order_product