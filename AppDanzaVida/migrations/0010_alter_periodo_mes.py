# Generated by Django 4.2.9 on 2024-01-19 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppDanzaVida', '0009_periodo_remove_cuota_nombre_detalleperiodo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='mes',
            field=models.CharField(choices=[('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')], max_length=20),
        ),
    ]
