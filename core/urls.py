from django.urls import path
from core import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .forms import FormularioLoginUsuario
from .views import agregar_producto, listar_productos, modificar_producto, eliminar_producto, listar_pedidos

# Validacion de usuario en login 
urlpatterns = [
    path('', views.VistaProducto.as_view(), name='inicio'),
    # Pagina del Carrito de Compras
    path('añadir-carrito/', views.añadir_carrito, name="añadir-carrito"),
    path('carrito/', views.mostrar_carrito, name="mostrar-carrito"),
    path('aumentarcarrito/', views.aumentar_carrito),
    path('reducircarrito/', views.reducir_carrito),
    path('removercarrito/', views.remover_carrito),
    #
    path('checkout/', views.verificar, name="verificar"),
    path('pagorealizado/', views.pago_realizado, name="pagorealizado"),
    path('ordenes/', views.ordenes, name='ordenes'),
    # 
    path('detalle-producto/<int:pk>', views.VistaDetalleProducto.as_view(), name='detalle-producto'),
    # 
    path('perfil/', views.VistaPerfil.as_view(), name='perfil'),
    #
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/test-login.html', authentication_form=FormularioLoginUsuario), name='login'),
    path('registro/', views.VistaRegistroCliente.as_view(), name="registrocliente"),
    path('cerrar-sesion/', auth_views.LogoutView.as_view(next_page='login'), name='cerrar-sesion'), # Cierra la sesion y redirige a la pagina de login
    # 
    path('contacto/', views.contacto, name='contacto'),
    # Pagina de los Telefonos
    path('telefono/', views.telefono, name='telefono'),
    path('telefono/<slug:data>', views.telefono, name='telefono'),
    # Pagina de los Audifonos
    path('audifono/', views.audifono, name='audifono'),
    path('audifono/<slug:data>', views.audifono, name='audifono'),
    # Pagina de los Computadores
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptop'),
    # Pagina de los Teclados
    path('teclado/', views.teclado, name='teclado'),
    path('teclado/<slug:data>', views.teclado, name='teclado'),
    path('direcciones/', views.direcciones, name='direcciones'),
    # 
    path('agregar-producto/', agregar_producto, name="agregar_producto"),
    path('listar-productos/', listar_productos, name="listar_productos"),
    path('modificar-producto/<id>/', modificar_producto, name="modificar_producto"),
    path('eliminar-producto/<id>/', eliminar_producto, name="eliminar_producto"),
    path('listar-pedidos/', listar_pedidos, name="listar_pedidos"),
    path('eliminar_pedido/<int:pedido_id>/', views.eliminar_pedido, name='eliminar_pedido'),
    # 
    path('clima-api-rest/', views.clima_api_rest, name="clima_api_rest"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)