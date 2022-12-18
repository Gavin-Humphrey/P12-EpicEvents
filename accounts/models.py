from random import choices
from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    MANAGEMENT = "MANAGEMENT"
    SALES = "SALES"
    SUPPORT = "SUPPORT"
   
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    team = models.CharField(
        choices = [
            (MANAGEMENT, MANAGEMENT),
            (SALES, SALES),
            (SUPPORT, SUPPORT)
        ],
        max_length=10,
        default=MANAGEMENT
    )

    def __str__(self):
        return f"{self.username} ({self.team})"

    def save(self, *args, **kwargs):
        if self.team == self.MANAGEMENT:
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False

        user = super(User, self)
        user.save()

        return user
