from django.contrib import admin
from django.urls import path
from inventario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('logout/', views.signout, name='logout'),
    path('registrar/', views.registrar_producto, name='registrar_producto'),
    path('entrada/', views.entrada_inventario, name='entrada_inventario'),
    path('salida/', views.salida_inventario, name='salida_inventario'),
]
