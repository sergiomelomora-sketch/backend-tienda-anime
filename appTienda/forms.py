# forms.py

from django import forms
from .models import Pedido
# widget con base input ayuda IA(chatgpt)
from django.forms.widgets import Input 


# uso de IA(chatgpt)
class MultipleFileInput(Input):
    input_type = 'file'
    
    def __init__(self, attrs=None):
        default_attrs = {'multiple': True}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


# hecho por el equipo
class PedidoSolicitudForm(forms.ModelForm):
    imagenes_referencia = forms.FileField(
        required=False,
        # mezcla de equipo y IA(chatgpt)
        widget=MultipleFileInput(), 
        label="Sube tus imágenes de referencia",
        help_text="Puedes seleccionar varias imágenes (bocetos, fotos de ejemplo, etc.)."
    )
    
    #hecho por el equipo
    contacto = forms.CharField(
        required=True, 
        label="Email y/o Teléfono y/o Usuario de Red Social",
        max_length=100
    )

    class Meta:
        model = Pedido
        fields = ['nombre_cliente', 'contacto', 'descripcion', 'fecha_solicitada']
        #ayuda IA(chatgpt)
        widgets = {
            'fecha_solicitada': forms.DateInput(attrs={'type': 'date', 'placeholder': 'AAAA-MM-DD'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
        #mezcla de equipo y dudas a la IA(chatgpt)
        labels = {
            'nombre_cliente': 'Tu Nombre Completo',
            'descripcion': 'Describe tu pedido personalizado',
            'fecha_solicitada': 'Fecha de entrega deseada (opcional)',
        }