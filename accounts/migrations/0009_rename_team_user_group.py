# Generated by Django 4.1.4 on 2022-12-29 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_alter_user_managers_alter_user_team"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="team",
            new_name="group",
        ),
    ]