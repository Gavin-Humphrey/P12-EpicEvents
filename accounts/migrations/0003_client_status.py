# Generated by Django 4.1.4 on 2022-12-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_team_client"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="status",
            field=models.BooleanField(default=False, verbose_name="Converted"),
        ),
    ]