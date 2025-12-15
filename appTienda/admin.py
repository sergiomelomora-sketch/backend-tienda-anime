from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Categoria, Producto, Insumo, Pedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'cantidad_disponible', 'unidad', 'marca', 'color')
    list_filter = ('tipo', 'marca', 'color')
    search_fields = ('nombre', 'marca')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_cliente',
        'producto',
        'estado',
        'estado_pago',
        'plataforma',
        'fecha_creacion'
    )

    list_filter = ('estado', 'estado_pago', 'plataforma', 'fecha_creacion')
    search_fields = ('nombre_cliente', 'contacto')
    def save_model(self, request, obj, form, change):
        if obj.estado == 'finalizada' and obj.estado_pago != 'pagado':
            raise ValidationError(
                'No se puede marcar un pedido como Finalizado si el pago no está Pagado.'
            )
        super().save_model(request, obj, form, change)

#Esto hace que el modelo Producto y Categoria sean gestionables desde el panel de administración de Django.