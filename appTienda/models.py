from django.db import models
import uuid #el uuid fue ayuda de IA(chatgpt)

#hecho por el equipo 
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

#hecho por el equipo
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen Principal")
    destacado = models.BooleanField(default=False, verbose_name="Producto Destacado")

    def __str__(self):
        return self.nombre

# hecho por el equipo
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos_adicionales/')
    
    class Meta: #ayuda IA(chatgpt)
        verbose_name = "Imagen Adicional de Producto"
        verbose_name_plural = "Imágenes Adicionales de Producto"

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

#hecho por el equipo
class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    cantidad_disponible = models.PositiveIntegerField() 
    unidad = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.color}" 
    
# hecho por el equipo 
class Pedido(models.Model):

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

    nombre_cliente = models.CharField(max_length=100)
    # hecho por el equipo 
    contacto = models.CharField(max_length=100) 
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
    )

    descripcion = models.TextField(verbose_name="Descripción de la Solicitud")

    #hecho por el equipo con mini consultas a la IA(Chatgpt)

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
        null=True,
        verbose_name="Fecha de Entrega Deseada"
    )

    token_seguimiento = models.UUIDField(
        default=uuid.uuid4,
        editable=False, 
        unique=True
    )
    #hecho solo por el equipo
    fecha_creacion = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente} ({self.estado})"
    

class ImagenReferencia(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='imagenes_referencia', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='pedidos_referencia/')
#mezcla de equiop e IA(Chatgpt)  
    class Meta:
        verbose_name = "Imagen de Referencia del Pedido"
        verbose_name_plural = "Imágenes de Referencia del Pedido"

    def __str__(self):
        return f"Referencia para Pedido #{self.pedido.id}"