from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)
from datetime import datetime




class UserManager(BaseUserManager):
    def _create_user(self, email, password=None,  **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        #user = self.create_user(email, password=password, **extra_fields)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


MANAGEMENT = "MANAGEMENT"
SALES = "SALES"
SUPPORT = "SUPPORT"
class User(AbstractUser):

    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    team = models.CharField(
    choices = [
            (MANAGEMENT, MANAGEMENT),
            (SALES, SALES),
            (SUPPORT, SUPPORT)
        ],
        max_length=20
    )
    username = None
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=25)
    mobile = models.CharField(max_length=25)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    sales_contact = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sales_contact')
    status = models.BooleanField(default=False, verbose_name="Converted")

    def __str__(self):
    
        if self.status is False:
            stat = "PROSPECT"
        else:
            stat = "CONVERTED"
        client_name = f"Client Nº{self.id} : {self.first_name} {self.last_name} - {self.email} ({stat})"    
        return client_name

    def update_date(self):
        self.date_updated = datetime.now()

    def save(self, *args, **kwargs):
        self.update_date()
        return super(Client, self).save()
