from django.contrib import admin
from .models import Cliente, Producto, Carrito, PedidoRealizado

# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'nombre', 'localidad', 'ciudad', 'codigo_postal', 'region']
    
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'precio_venta', 'descripcion', 'marca', 'categoria', 'imagen_producto']
    
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'producto', 'cantidad']
    
@admin.register(PedidoRealizado)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cliente', 'producto', 'cantidad', 'fecha_pedido', 'estado']