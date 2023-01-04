# Generated by Django 4.1.4 on 2023-01-04 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0001_initial"),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="contract",
            field=models.OneToOneField(
                limit_choices_to={"is_signed": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="event",
                to="contracts.contract",
            ),
        ),
    ]
