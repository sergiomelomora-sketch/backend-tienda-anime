from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.forms.widgets import Input
from .models import Pedido

class MultipleFileInput(Input):
    input_type = 'file'

    def __init__(self, attrs=None):
        default_attrs = {'multiple': True}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

class PedidoSolicitudForm(forms.ModelForm):
    imagenes_referencia = forms.FileField(
        required=False,
        widget=MultipleFileInput(),
        label="Sube tus imágenes de referencia",
        help_text="Puedes seleccionar varias imágenes (bocetos, fotos de ejemplo, etc.)."
    )

    contacto = forms.CharField(
        required=True,
        label="Email y/o Teléfono y/o Usuario de Red Social",
        max_length=100
    )

    class Meta:
        model = Pedido
        fields = [
            'nombre_cliente',
            'contacto',
            'descripcion',
            'fecha_solicitada'
        ]
        widgets = {
            'fecha_solicitada': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'AAAA-MM-DD'}
            ),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'nombre_cliente': 'Tu Nombre Completo',
            'descripcion': 'Describe tu pedido personalizado',
            'fecha_solicitada': 'Fecha de entrega deseada (opcional)',
        }

    def clean_fecha_solicitada(self):
        fecha = self.cleaned_data.get('fecha_solicitada')

        if fecha and fecha < timezone.now().date():
            raise ValidationError(
                "No puedes seleccionar una fecha que ya haya pasado."
            )

        return fecha
