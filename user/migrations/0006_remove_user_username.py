# Generated by Django 4.2.2 on 2023-06-13 07:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_user_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]
