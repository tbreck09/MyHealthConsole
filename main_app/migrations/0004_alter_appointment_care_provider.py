# Generated by Django 4.2.4 on 2023-08-17 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_appointment_care_provider_appointment_purpose_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='care_provider',
            field=models.CharField(max_length=75, null=True),
        ),
    ]
