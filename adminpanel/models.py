from django.db import models
# Create your models here.

class Departments(models.Model):
    name = models.CharField(max_length= 255)
    fee = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    

    def __str__(self):
        return  self.name  


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    experience = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    available = models.BooleanField(default=True)
    depart = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True)
    department = models.CharField(max_length=225,null=True,blank=True)

    
    def __str__(self):
        return self.name 
    
