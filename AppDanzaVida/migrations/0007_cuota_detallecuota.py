# Generated by Django 4.2.9 on 2024-01-17 21:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AppDanzaVida', '0006_remove_disciplina_cantidad_horas_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_generacion', models.DateField(default=django.utils.timezone.now)),
                ('fecha_vencimiento', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCuota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=6)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppDanzaVida.alumno')),
                ('cuota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='AppDanzaVida.cuota')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppDanzaVida.disciplina')),
            ],
        ),
    ]
