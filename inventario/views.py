from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import ProductoForm, EntradaInventarioForm, SalidaInventarioForm, ProductoSearchForm, EditarProductoForm
from inventario.models import Producto
from .models import Producto

def check_authenticated(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        return view_func(request, *args, **kwargs)
    return wrapped_view

@login_required
def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user
            producto.full_clean()
            producto.save()
            messages.success(request, "Producto registrado con éxito.")
            return redirect('home')
        else:
            messages.error(request, "Error en el formulario.")
    else:
        form = ProductoForm()
    return render(request, 'registrar_producto.html', {'form': form})

@check_authenticated
def entrada_inventario(request):
    if request.method == 'POST':
        form = EntradaInventarioForm(request.POST, user=request.user)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']

            producto.existencias += cantidad
            producto.save()

            messages.success(request, "Producto agregado correctamente al inventario.")
            return redirect('home')
        else:
            messages.error(request, "Error en el formulario.")
    else:
        form = EntradaInventarioForm(user=request.user)

    return render(request, 'entrada_inventario.html', {'form': form})


@check_authenticated
def salida_inventario(request):
    if request.method == 'POST':
        form = SalidaInventarioForm(request.POST, user=request.user)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            if cantidad <= producto.existencias:
                producto.existencias -= cantidad
                producto.save()
                messages.success(request, "Producto retirado correctamente del inventario.")
                return redirect('home')
            else:
                form.add_error('cantidad', 'No hay suficiente stock.')
                messages.error(request, "No hay suficiente stock disponible.")
        else:
            messages.error(request, "Error en el formulario.")
    else:
        form = SalidaInventarioForm(user=request.user)
    return render(request, 'salida_inventario.html', {'form': form})

@login_required
def home(request):
    productos = Producto.objects.filter(usuario=request.user)
    return render(request, 'home.html', {'productos': productos})

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                return redirect('signin')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "El usuario ya existe"
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'La contraseña con coincide'
        })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        username = request.POST.get('usuario')
        password = request.POST.get('contrasena')

        if not username or not password:
            messages.error(request, 'Usuario y contraseña son obligatorios.')
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'show_sweetalert': True
            })

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'El usuario o contraseña es incorrecto')
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'show_sweetalert': True
            })
        else:
            login(request, user)
            return redirect('home')

def signout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('signin'))
    response.delete_cookie('sessionid')
    return response

@check_authenticated
def lista_productos(request):
    form = ProductoSearchForm(request.GET)
    productos = Producto.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            productos = productos.filter(descripcion__icontains=search_query)

    context = {'productos': productos, 'form': form}
    return render(request, 'lista_productos.html', context)

@check_authenticated
def buscar_producto(request):
    query = request.GET.get('q')
    productos = Producto.objects.filter(usuario=request.user, descripcion__icontains=query)
    return render(request, 'home.html', {'productos': productos})

@check_authenticated
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_del_producto=producto_id)
    if request.method == 'POST':
        form = EditarProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditarProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})


