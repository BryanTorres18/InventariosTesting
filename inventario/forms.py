from django import forms
from django.contrib.auth import authenticate

from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['descripcion', 'referencias', 'existencias', 'costo', 'precio']

class EntradaInventarioForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.none(), label="Seleccione un Producto")
    cantidad = forms.IntegerField(min_value=1, label='Cantidad a ingresar')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(usuario=user)

class SalidaInventarioForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.none(), label="Seleccione un Producto")
    cantidad = forms.IntegerField(min_value=1, label='Cantidad a sacar')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(usuario=user)

