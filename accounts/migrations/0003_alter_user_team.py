# Generated by Django 4.1.4 on 2022-12-27 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="team",
            field=models.CharField(
                choices=[
                    ("MANAGEMENT", "Management"),
                    ("SALES", "Sales"),
                    ("SUPPORT", "Support"),
                    ("NONE", "None"),
                ],
                default="NONE",
                max_length=150,
                verbose_name="Team",
            ),
        ),
    ]