from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Cliente, Producto, Carrito, PedidoRealizado
from .forms import FormularioRegistroUsuario, FormularioPerfilCliente, FormularioContacto, ProductoForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

# Vista de la lista de Productos (PRINCIPAL)
class VistaProducto(View):
    def get(self, request):
        audifonos = Producto.objects.filter(categoria='A')
        laptop = Producto.objects.filter(categoria='L')
        mobiles = Producto.objects.filter(categoria='M')
        teclados = Producto.objects.filter(categoria='T')
        return render(request, 'core/inicio.html', {'audifonos':audifonos, 'laptop':laptop, 'mobiles':mobiles, 'teclados':teclados})
    
# Vista del Detalle del Producto
class VistaDetalleProducto(View):
    def get(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        return render(request, 'core/detalle-producto.html', {'producto':producto})
    
# Vista del Carrito de Compras
@login_required
def añadir_carrito(request):
    user = request.user
    producto_id = request.GET.get('prod_id')
    producto = Producto.objects.get(id=producto_id)
    Carrito(user=user, producto=producto).save()
    return redirect('/carrito')

# Vista para Mostrar el Carrito de Compras
@login_required
def mostrar_carrito(request):
    if request.user.is_authenticated:
        user = request.user
        carrito = Carrito.objects.filter(user=user)
        # Calculo matematico para lograr sumar la cantidad de productos en el carrito y sumando el costo de envio.
        pago = 0
        envio = 2000
        total_pago = 0
        productos_carrito = [p for p in Carrito.objects.all() if p.user == user]
        if productos_carrito:
            for p in productos_carrito:
               total_temporal = (p.cantidad * p.producto.precio_venta) 
               pago += total_temporal
               total_pago = pago + envio
            return render(request, 'core/añadir-carrito.html', {'carritos':carrito, 'total_pago':total_pago, 'pago':pago, 'envio':envio})
        else:
            return render(request, 'core/carrito-vacio.html')

# Funcion para aumentar productos del carrito
def aumentar_carrito(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Carrito.objects.get(Q(producto=prod_id) & Q(user=request.user))
        c.cantidad += 1
        c.save()
        pago = 0
        envio = 2000
        productos_carrito = [p for p in Carrito.objects.all() if p.user == request.user]
        for p in productos_carrito:
            total_temporal = (p.cantidad * p.producto.precio_venta) 
            pago += total_temporal
            
            data = {
                'cantidad': c.cantidad,
                'pago': pago,
                'total_pago': pago + envio
            }
        return JsonResponse(data)
   
# Funcion para reducir productos del carrito 
def reducir_carrito(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Carrito.objects.get(Q(producto=prod_id) & Q(user=request.user))
        c.cantidad -= 1
        c.save()
        pago = 0
        envio = 2000
        productos_carrito = [p for p in Carrito.objects.all() if p.user == request.user]
        for p in productos_carrito:
            total_temporal = (p.cantidad * p.producto.precio_venta) 
            pago += total_temporal
            
            data = {
                'cantidad': c.cantidad,
                'pago': pago,
                'total_pago': pago + envio
            }
        return JsonResponse(data)
    
# Funcion para remover productos del carrito 
def remover_carrito(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Carrito.objects.get(Q(producto=prod_id) & Q(user=request.user))
        c.delete()
        pago = 0
        envio = 2000
        productos_carrito = [p for p in Carrito.objects.all() if p.user == request.user]
        for p in productos_carrito:
            total_temporal = (p.cantidad * p.producto.precio_venta) 
            pago += total_temporal
            
            data = {
                'pago': pago,
                'total_pago': pago + envio
            }
        return JsonResponse(data)

# Funcion del Checkout
@login_required
def verificar(request):
    user = request.user
    add = Cliente.objects.filter(user=user)
    items_carrito = Carrito.objects.filter(user=user)
    pago = 0
    envio = 2000
    total_pago = 0
    productos_carrito = [p for p in Carrito.objects.all() if p.user == request.user]
    if productos_carrito:
        for p in productos_carrito:
            total_temporal = (p.cantidad * p.producto.precio_venta) 
            pago += total_temporal
        total_pago = pago + envio
    return render(request, 'core/verificar.html', {'add':add, 'total_pago':total_pago, 'items_carrito':items_carrito})

# Funcion del pago realizado
@login_required
def pago_realizado(request):
    user = request.user
    custid = request.GET.get('custid')
    cliente = Cliente.objects.get(id=custid)
    carrito = Carrito.objects.filter(user=user)
    for c in carrito:
        PedidoRealizado(user=user, cliente=cliente, producto=c.producto, cantidad=c.cantidad).save()
        c.delete()
    return redirect("ordenes")

# Funcion de las ordenes
@login_required
def ordenes(request):
    pedidos = PedidoRealizado.objects.select_related('producto').filter(user=request.user)
    # pd = PedidoRealizado.objects.filter(user=request.user)
    return render(request, 'core/ordenes.html', {'pedidos':pedidos})
        
# Vista del Registro de Usuario
class VistaRegistroCliente(View):
    def get(self, request):
        formulario = FormularioRegistroUsuario()
        return render(request, 'core/test-registro.html', {'formulario':formulario})
    
    def post(self, request):
        formulario = FormularioRegistroUsuario(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Registrado Correctamente, Recuerda Registrar Tu Direccion En Tu Perfil')
            return redirect(reverse('login'))
        return render(request, 'core/test-registro.html', {'formulario':formulario})
    
# Vista del Perfil
@method_decorator(login_required, name='dispatch')
class VistaPerfil(View):
    def get(self, request):
        form = FormularioPerfilCliente()
        return render(request, 'core/perfil.html', {'form':form,
        'active':'btn-primary'})
        
    def post(self, request):
        form = FormularioPerfilCliente(request.POST)
        if form.is_valid():
            usr = request.user
            nombre = form.cleaned_data['nombre']
            localidad = form.cleaned_data['localidad']
            ciudad = form.cleaned_data['ciudad']
            region = form.cleaned_data['region']
            codigo_postal = form.cleaned_data['codigo_postal']
            reg = Cliente(user=usr, nombre=nombre, localidad=localidad, ciudad=ciudad, region=region, codigo_postal=codigo_postal)
            reg.save()
            messages.success(request, 'Direccion Registrada Correctamente')
            form = FormularioPerfilCliente()  # Limpiar los campos del formulario
        return render(request, 'core/perfil.html', {'form':form,
        'active':'btn-primary'})
        
# Vista de los Audifonos
def audifono(request, data=None):
    if data == None:
        audifonos = Producto.objects.filter(categoria='A')
    return render(request, 'core/audifonos.html', {'audifonos':audifonos})

# Vista de los Laptop
def laptop(request, data=None):
    if data == None:
        laptops = Producto.objects.filter(categoria='L')
    return render(request, 'core/laptops.html', {'laptops':laptops})

# Vista del Telefono
def telefono(request, data=None):
    if data == None:
        telefonos = Producto.objects.filter(categoria='M')
    return render(request, 'core/telefono.html', {'telefonos':telefonos})

# Vista de los Teclados
def teclado(request, data=None):
    if data == None:
        teclados = Producto.objects.filter(categoria='T')
    return render(request, 'core/teclados.html', {'teclados':teclados})

# Vista de Formulario de Contacto
def contacto_vista (request):
    if request.method == 'POST':
        form = FormularioContacto(request.POST)
        if form.is_valid():
            messages.success(request, '¡Se ha enviado con exito!, nos comunicaremos con usted lo antes posible.')
            form.save()
            return render(request, 'contacto.html')
    else:
        form = FormularioContacto()
    return render(request, 'core/contacto.html', {'form': form})

# Vista del Contacto
def contacto(request):
    return render(request, 'core/contacto.html')

@login_required
# Vista de las Direcciones
def direcciones(request):
    agregar = Cliente.objects.filter(user=request.user)
    return render(request, 'core/direcciones.html', {'agregar':agregar, 'active':'btn-primary'})


# Vista para agregar producto para el admin
@staff_member_required
def agregar_producto(request):
    
    data = {
        'form': ProductoForm()
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado Correctamente"
        else:
            data["form"] = formulario
    
    return render(request, 'core/admin/agregar.html', data)

# Vista para listar productos para el admin
@staff_member_required
def listar_productos(request):
    productos = Producto.objects.all()
    
    data = {
        'productos': productos
    }
    return render(request, 'core/admin/listar.html', data)

# Vistar para editar productos para el admin
@staff_member_required
def modificar_producto(request, id):
    
    producto = get_object_or_404(Producto, id=id)
    
    data = {
        'form': ProductoForm(instance=producto)
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to='listar_productos')
        data["form"] = formulario
        
    return render(request, 'core/admin/modificar.html', data)

# Vista para eliminar productos para el admin
@staff_member_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_productos")

# Vista para poder listar los pedidos que se han realizado en la pagina
@staff_member_required
def listar_pedidos(request):
    pedidos = PedidoRealizado.objects.all()
    return render(request, 'core/admin/listar-pedidos.html', {'pedidos':pedidos})

# Vista para poder eliminar un pedido realizado
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(PedidoRealizado, id=pedido_id)
    pedido.delete()
    return redirect('listar_pedidos')


# Vista de la pagina de de la api rest
def clima_api_rest(request):
    return render(request, 'core/clima-api-rest.html')