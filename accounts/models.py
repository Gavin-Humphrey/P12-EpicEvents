from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser, Group
)
from datetime import datetime



use_in_migrations = True

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None,  **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password=None, **extra_fields):
        """Create and save a staff User with the given email and password."""
        if email is None:
            raise TypeError('Users must have an email address')

        user = self.create_user(username, email, password)
        user.is_superuser = False
        user.is_staff = True
        user.team = "SALES" #group
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, and password.
        """
        if email is None:
            raise TypeError('Users must have an email address')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.team = "MANAGEMENT"
        user.save(using=self._db)
        return user


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
        max_length=20,
    )
    #username = None
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    readonly_fields = ['date_created', 'date_updated']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    
    

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
        client_name = f"Client Nº{self.id} : {self.first_name} - {self.last_name}  ({stat})"    
        return client_name

    def update_date(self):
        self.date_updated = datetime.now()

    def save(self, *args, **kwargs):
        self.update_date()
        return super(Client, self).save()
