from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from django.contrib.auth.models import User
class Producto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="productos")
    id_del_producto = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    referencias = models.TextField()
    existencias = models.IntegerField(validators=[MaxValueValidator(2147483647)])
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        super().clean()
        if not self.id_del_producto:
            if Producto.objects.filter(descripcion=self.descripcion, referencias=self.referencias).exists():
                raise ValidationError('Ya existe un producto con esta descripción y referencias.')

        if self.costo >= self.precio:
            raise ValidationError('El costo debe ser menor que el precio.')

        if self.existencias < 0:
            raise ValidationError('No  de un producto con existencias menores a 0.')

        if len(self.referencias) > 100:
            raise ValidationError('La referencia del producto es demasiado larga.')

    def __str__(self):
        return f"{self.descripcion} (Referencias: {self.referencias})"
