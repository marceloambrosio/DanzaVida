# Generated by Django 4.2.9 on 2024-01-17 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppDanzaVida', '0007_cuota_detallecuota'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallecuota',
            name='pagada',
            field=models.BooleanField(default=False),
        ),
    ]
