import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(max_length=100)),
                ('cantidad_disponible', models.PositiveIntegerField()),
                ('unidad', models.CharField(blank=True, max_length=50, null=True)),
                ('marca', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio_base', models.DecimalField(decimal_places=2, max_digits=8)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos/')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appTienda.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('contacto', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('imagen_referencia', models.ImageField(blank=True, null=True, upload_to='pedidos/')),
                ('plataforma', models.CharField(choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('whatsapp', 'WhatsApp'), ('presencial', 'Presencial'), ('sitio_web', 'Sitio Web'), ('otra', 'Otra')], max_length=20)),
                ('estado', models.CharField(choices=[('solicitado', 'Solicitado'), ('aprobado', 'Aprobado'), ('en_proceso', 'En proceso'), ('realizada', 'Realizada'), ('entregada', 'Entregada'), ('finalizada', 'Finalizada'), ('cancelada', 'Cancelada')], default='solicitado', max_length=20)),
                ('estado_pago', models.CharField(choices=[('pendiente', 'Pendiente'), ('parcial', 'Parcial'), ('pagado', 'Pagado')], default='pendiente', max_length=20)),
                ('fecha_solicitada', models.DateField(blank=True, null=True)),
                ('token_seguimiento', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appTienda.producto')),
            ],
        ),
    ]
