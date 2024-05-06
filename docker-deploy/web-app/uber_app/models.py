from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email_address, user_name, password=None, **extra_fields):
        if not email_address:
            raise ValueError('The Email Address must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email_address=email_address, user_name=user_name, password=password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True)
    email_address = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(_('user name'), max_length=255, unique=True)
    is_driver = models.BooleanField(default=False, blank=True, null=False)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email_address']

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name

# class User(models.Model):
#     user_id = models.BigAutoField(primary_key=True)
#     email_address = models.CharField(max_length=255)
#     user_name = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     is_driver = models.BooleanField(default=False, blank=True, null=False)
    
#     def __str__(self):
#         return self.user_name
    
    # @property
    # def check_is_driver(self):
    #     return self.is_driver

class Vehicle(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=255)
    license_plate = models.CharField(max_length=255)
    max_passengers = models.IntegerField()
    special_vehicle_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.license_plate

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(Vehicle, self).save(*args, **kwargs)
        # Automatically set the driver as a driver when a Vehicle instance is saved
        if not self.driver.is_driver:
            self.driver.is_driver = True
            self.driver.save()

class Ride(models.Model):
    ride_id = models.BigAutoField(primary_key=True)
    destination = models.CharField(max_length=255)
    required_arrival_date_time = models.DateTimeField()
    vehicle_type = models.CharField(max_length=255, blank=True, null=True)
    special_request = models.CharField(max_length=255, blank=True, null=True)
    shared = models.BooleanField()
    status = models.CharField(max_length=255)
    driver = models.ForeignKey(User, related_name='rides_driven', on_delete=models.SET_NULL, null=True, blank=True)
    #ownerID = models.ForeignKey(User, related_name='rides_owned', on_delete=models.CASCADE)
    #ownerID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ownerID = models.BigIntegerField()
    owner_passenger_num = models.IntegerField()

    def __str__(self):
        return f"{self.destination} ({self.status})"

class RideSharer(models.Model):
    share_ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    share_user = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger_num = models.IntegerField()

    def __str__(self):
        return f"{self.share_user.user_name}"# - {self.share_ride.destination}"