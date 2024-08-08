# Generated by Django 4.2.9 on 2024-08-08 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppDanzaVida', '0006_detallecuota_movimiento_caja'),
    ]

    operations = [
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo_postal', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='alumno',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alumnos', to='AppDanzaVida.localidad'),
        ),
    ]
