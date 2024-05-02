from django.db import models

from django.contrib.auth.models import User
class Producto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="productos")
    id_del_producto = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    referencias = models.TextField()
    existencias = models.IntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descripcion} (Referencias: {self.referencias})"
