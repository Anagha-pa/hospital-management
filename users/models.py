from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from adminpanel.models import Doctor




class UserAccountManager(BaseUserManager):
  def create_user(self, first_name, last_name, email, password=None):
    if not email:
      raise ValueError('Users must have an email address')

    email = self.normalize_email(email)
    email = email.lower()

    user = self.model(
      first_name=first_name,
      last_name=last_name,
      email=email,
    )

    user.set_password(password)
    user.save(using=self._db)

    return user
  
  
  def create_superuser(self, first_name, last_name, email, password=None):
    if password is None:
      raise TypeError("Superusers must have a password.")
    
    user = self.create_user(
      first_name,
      last_name,
      email,
      password=password,
    )

    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)

    return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField(unique=True, max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  otp=models.CharField(max_length=6,null=True,blank=True)
  otp_verified = models.BooleanField(default=False)
  age = models.PositiveIntegerField(null=True, blank=True)
  gender = models.CharField(max_length=6,default="male")
  phone_number = models.CharField(max_length=15, null=True, blank=True)
  address = models.TextField(null=True, blank=True)
  

 
  objects = UserAccountManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']


class Appointment(models.Model):
  first_name = models.CharField(max_length=255, null=True, blank=True)
  last_name = models.CharField(max_length=255, null=True, blank=True)
  age = models.PositiveIntegerField(null=True, blank=True)
  gender = models.CharField(max_length=6,default="male")
  phone_number = models.CharField(max_length=15, null=True, blank=True)
  address = models.TextField(null=True, blank=True)
  department = models.CharField(max_length=255, null=True, blank=True)
  doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True, blank=True)
  slot_date = models.DateTimeField(null=True,blank=True)
  payment_status = models.BooleanField(default=False)
  fee = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
  user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
  


  def __str__(self):
    return self.first_name
  

  
