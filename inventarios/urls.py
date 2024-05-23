from django.contrib import admin

from django.contrib.auth.decorators import login_required
from django.urls import path, include
from inventario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', login_required(views.home), name='home'),
    path('logout/', views.signout, name='logout'),
    path('registrar/', login_required(views.registrar_producto), name='registrar_producto'),
    path('entrada/', login_required(views.entrada_inventario), name='entrada_inventario'),
    path('salida/', login_required(views.salida_inventario), name='salida_inventario'),
    path('buscar_producto/', login_required(views.buscar_producto), name='buscar_producto'),
    path('editar_producto/<int:producto_id>/', login_required(views.editar_producto), name='editar_producto'),
    path('lista_productos/', login_required(views.lista_productos), name='lista_productos')
]
