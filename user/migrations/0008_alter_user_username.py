# Generated by Django 4.2.2 on 2023-06-14 20:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0007_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                blank=True,
                max_length=150,
                null=True,
                unique=True,
                verbose_name="username",
            ),
        ),
    ]