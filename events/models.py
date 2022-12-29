from django.db import models
from accounts.models import User, Client
from contracts.models import Contract




class Event(models.Model):

    CREATED = 'created'
    INPROGRESS = 'in_progress'
    FINISHED = 'finished'
    EVENT_STATUS = [
        (CREATED, 'created'),
        (INPROGRESS, 'in_progress'),
        (FINISHED, 'finished')
    ]
    id = models.BigAutoField(primary_key=True)
    support_contact = models.ForeignKey(to=User, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    event_status = models.CharField(choices=EVENT_STATUS, max_length=20, default=CREATED)

    attendees = models.IntegerField(default=0)
    event_date = models.DateTimeField(auto_now_add=False)

    notes = models.TextField(null=True, blank=True)

