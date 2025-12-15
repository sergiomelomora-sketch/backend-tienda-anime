from django.db import models
import uuid

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    cantidad_disponible = models.PositiveIntegerField() #evita números negativos
    unidad = models.CharField(max_length=50, blank=True, null=True) #opcional (ej: kg, metros, unidades)
    marca = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.color}" #mejora la visualización en el Admin
    
class Pedido(models.Model):

    # ----- CHOICES -----
    ESTADO_PEDIDO = [
        ('solicitado', 'Solicitado'),
        ('aprobado', 'Aprobado'),
        ('en_proceso', 'En proceso'),
        ('realizada', 'Realizada'),
        ('entregada', 'Entregada'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    ESTADO_PAGO = [
        ('pendiente', 'Pendiente'),
        ('parcial', 'Parcial'),
        ('pagado', 'Pagado'),
    ]

    PLATAFORMA = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('whatsapp', 'WhatsApp'),
        ('presencial', 'Presencial'),
        ('sitio_web', 'Sitio Web'),
        ('otra', 'Otra'),
    ]

    # ----- DATOS DEL CLIENTE -----
    nombre_cliente = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)

    # ----- PRODUCTO -----
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL, #no rompe pedidos si borran un producto
        null=True,
        blank=True
    )

    descripcion = models.TextField()

    # ----- IMÁGENES -----
    imagen_referencia = models.ImageField(
        upload_to='pedidos/',
        blank=True,
        null=True
    )

    # ----- CONTROL -----
    plataforma = models.CharField(
        max_length=20,
        choices=PLATAFORMA
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_PEDIDO,
        default='solicitado'
    )

    estado_pago = models.CharField(
        max_length=20,
        choices=ESTADO_PAGO,
        default='pendiente'
    )

    fecha_solicitada = models.DateField(
        blank=True,
        null=True
    )

    # ----- TOKEN -----
    token_seguimiento = models.UUIDField( #token único y seguro
        default=uuid.uuid4,
        editable=False, #no se cambia manualmente
        unique=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.nombre_cliente}"

