from django.db import models
from accounts.models import User, SUPPORT
from contracts.models import Contract


class Event(models.Model):
    class EventSatuts(models.TextChoices):
        CREATED = "CREATED"
        INPROGRESS = "INPROGRESS"
        FINISHED = "FINISHED"

    id = models.BigAutoField(primary_key=True)
    contract = models.OneToOneField(
        to=Contract,
        on_delete=models.CASCADE,
        limit_choices_to={"is_signed": True},
        related_name="event",
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    support_contact = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        limit_choices_to={"team": SUPPORT},
        related_name="event",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    event_status = models.CharField(
        max_length=100,
        verbose_name="Event Status",
        choices=EventSatuts.choices,
        default=EventSatuts.CREATED,
    )
    attendees = models.IntegerField(default=0)
    event_date = models.DateTimeField(auto_now_add=False)

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        name = f"{self.contract.client.last_name}, {self.contract.client.first_name}"
        date = self.event_date.strftime("%Y-%m-%d")

        return f"Event #{self.id} : {name} | Date : {date} ({self.event_status})"
