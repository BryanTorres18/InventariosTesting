from django import forms
from django.core.exceptions import ValidationError
import re

from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['descripcion', 'referencias', 'existencias', 'costo', 'precio']
        widgets = {
            'existencias': forms.NumberInput(attrs={'min': '1'}),
            'costo': forms.NumberInput(attrs={'min': '0.01'}),
            'precio': forms.NumberInput(attrs={'min': '0.01'}),
        }

    def clean_referencias(self):
        referencias = self.cleaned_data.get('referencias')
        if not re.match(r'^[\w\s]+$', referencias):
            raise ValidationError('Las referencias solo pueden contener letras, números y espacios.')

        return referencias

    def clean(self):
        cleaned_data = super().clean()
        costo = cleaned_data.get('costo')
        precio = cleaned_data.get('precio')

        if costo and precio and costo >= precio:
            raise forms.ValidationError('El costo debe ser menor que el precio.')

        return cleaned_data

class EntradaInventarioForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.none(), label="Seleccione un Producto")
    cantidad = forms.IntegerField(min_value=1, label='Cantidad a ingresar')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(usuario=user)

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        producto = self.cleaned_data.get('producto')

        if producto:
            if cantidad + producto.existencias > 2147483647:
                raise ValidationError("La cantidad a ingresar supera el límite permitido.")

        return cantidad

class SalidaInventarioForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.none(), label="Seleccione un Producto")
    cantidad = forms.IntegerField(min_value=1, label='Cantidad a sacar')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(usuario=user)

class ProductoSearchForm(forms.Form):
    query = forms.CharField(label='Buscar Producto', max_length=100)

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['descripcion', 'referencias', 'existencias', 'costo', 'precio']
        widgets = {
            'existencias': forms.NumberInput(attrs={'min': '0'}),
            'costo': forms.NumberInput(attrs={'min': '0.01'}),
            'precio': forms.NumberInput(attrs={'min': '0.01'}),
        }
