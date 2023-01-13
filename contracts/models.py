from django.db import models
from accounts.models import User, Client, SALES


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"team": SALES},
    )
    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, limit_choices_to={"status": True},
    related_name='contract'
    )
    is_signed = models.BooleanField(default=False, verbose_name="is_signed")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    payment_due = models.DateField()

    def __str__(self):
        name = f"{self.client.last_name}, {self.client.first_name}"
        due = self.payment_due.strftime("%Y-%m-%d")
        if self.is_signed is False:
            stat = "NOT SIGNED"
        else:
            stat = "IS_SIGNED"

        return f"Contract Nº{self.id} : {name} | Due : {due} ({stat})"
