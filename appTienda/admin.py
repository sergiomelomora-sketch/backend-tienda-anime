# appTienda/admin.py
#hecho por el equipo
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html 

from .models import Categoria, Producto, ImagenProducto, Insumo, Pedido, ImagenReferencia 


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1 
    max_num = 3 
    readonly_fields = ('miniatura',)

    def miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.imagen.url)
        return "Sin Imagen"
    miniatura.short_description = "Vista Previa"


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base', 'destacado', 'mostrar_imagen_principal')
    list_filter = ('categoria', 'destacado')
    search_fields = ('nombre', 'descripcion')
    
# uso de IA (chatgpt)
    inlines = [ImagenProductoInline]

# hecho por el equipo
    def mostrar_imagen_principal(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.imagen.url)
        return "Sin Imagen"
    mostrar_imagen_principal.short_description = "Miniatura"


@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'cantidad_disponible', 'unidad', 'marca', 'color')
    list_filter = ('tipo', 'marca', 'color')
    search_fields = ('nombre', 'marca')


# uso de IA(chatgpt)
class ImagenReferenciaInline(admin.TabularInline):
    model = ImagenReferencia
    extra = 1
    
#hecho por el equipo, menos el inlines que fue ayuda de IA(chatgpt)
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_cliente',
        'producto',
        'mostrar_estado_coloreado', 
        'estado_pago',
        'plataforma',
        'fecha_solicitada',
        'fecha_creacion'
    )
    list_display_links = ('id', 'nombre_cliente')
    inlines = [ImagenReferenciaInline]
    
    
    readonly_fields = ('token_seguimiento', 'fecha_creacion')
    
    fields = (
        'nombre_cliente',
        'contacto',
        'producto',
        'descripcion',
        'plataforma',
        'estado',
        'estado_pago',
        'fecha_solicitada',
        'token_seguimiento',
        'fecha_creacion',
    )

    
    list_filter = ('estado', 'estado_pago', 'plataforma', 'fecha_solicitada', 'fecha_creacion')
    search_fields = ('nombre_cliente', 'contacto')
    
    # Uso de IA(chatgpt)
    def save_model(self, request, obj, form, change):
        if obj.estado == 'finalizada' and obj.estado_pago != 'pagado':
            raise ValidationError(
                'No se puede marcar un pedido como Finalizado si el pago no está Pagado.'
            )
        super().save_model(request, obj, form, change)
        
    # mezcla de trabajo del grupo y de dudas a la IA(chatgpt)
    def mostrar_estado_coloreado(self, obj):
        colores = {
            'solicitado': 'blue',     
            'aprobado': 'lightblue',  
            'en_proceso': 'orange',   
            'realizada': 'purple',    
            'entregada': 'green',     
            'finalizada': 'darkgreen',
            'cancelada': 'red',       
        }
        color = colores.get(obj.estado, 'gray')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display() 
        )
        
    mostrar_estado_coloreado.short_description = 'Estado'
    mostrar_estado_coloreado.admin_order_field = 'estado'