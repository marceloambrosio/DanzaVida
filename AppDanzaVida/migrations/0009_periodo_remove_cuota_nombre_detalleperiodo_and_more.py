# Generated by Django 4.2.9 on 2024-01-19 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppDanzaVida', '0008_detallecuota_pagada'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(max_length=20)),
                ('anio', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='cuota',
            name='nombre',
        ),
        migrations.CreateModel(
            name='DetallePeriodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_nombre', models.CharField(max_length=20)),
                ('dia_numero', models.PositiveIntegerField()),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='AppDanzaVida.periodo')),
            ],
        ),
        migrations.AddField(
            model_name='cuota',
            name='periodo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cuotas', to='AppDanzaVida.periodo'),
            preserve_default=False,
        ),
    ]
