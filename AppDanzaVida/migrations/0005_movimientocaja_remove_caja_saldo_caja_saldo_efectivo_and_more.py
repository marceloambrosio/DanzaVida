# Generated by Django 4.2.9 on 2024-04-06 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppDanzaVida', '0004_alter_detallecuota_monto'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pago', models.CharField(choices=[('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia')], max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='caja',
            name='saldo',
        ),
        migrations.AddField(
            model_name='caja',
            name='saldo_efectivo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='caja',
            name='saldo_transferencia',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='categoriacaja',
            name='tipo',
            field=models.CharField(choices=[('Ingreso', 'Ingreso'), ('Egreso', 'Egreso')], max_length=20),
        ),
        migrations.DeleteModel(
            name='DetalleCaja',
        ),
        migrations.AddField(
            model_name='movimientocaja',
            name='caja',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalle_caja', to='AppDanzaVida.caja'),
        ),
        migrations.AddField(
            model_name='movimientocaja',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalle_caja', to='AppDanzaVida.categoriacaja'),
        ),
    ]
