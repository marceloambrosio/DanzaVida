# Generated by Django 4.2.9 on 2024-01-20 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppDanzaVida', '0013_rename_persente_detalleasistencia_presente'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleperiodo',
            name='asistencia_tomada',
            field=models.BooleanField(default=False),
        ),
    ]
