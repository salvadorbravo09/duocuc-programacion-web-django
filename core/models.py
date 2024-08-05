from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

# Modelo del Cliente
REGION_CHOISES = (
    ("I	Región de Tarapacá", "I	Región de Tarapacá"),
    ("II Región de Antofagasta", "II Región de Antofagasta"),
    ("III Región de Atacama", "III Región de Atacama"),
    ("IV Región de Coquimbo", "IV Región de Coquimbo"),
    ("V Región de Valparaíso", "V Región de Valparaíso"),
    ("VI Región del Libertador General Bernardo OHiggins", "VI Región del Libertador General Bernardo OHiggins"),
    ("VII Región del Maule", "VII Región del Maule"),
    ("VIII Región del Bio-bío", "VIII Región del Bio-bío"),
    ("IX Región de La Araucanía", "IX Región de La Araucanía"),
    ("X Región de Los Lagos", "X Región de Los Lagos"),
    ("XI Región Aysén del General Carlos Ibáñez del Campo", "XI Región Aysén del General Carlos Ibáñez del Campo"),
    ("XII Región de Magallanes y Antártica Chilena", "XII Región de Magallanes y Antártica Chilena"),
    ("Región Metropolitana de Santiago", "Región Metropolitana de Santiago"),
    ("XIV Región de Los Ríos", "XIV Región de Los Ríos"),
    ("XV Región de Arica y Parinacota", "XV Región de Arica y Parinacota"),
    ("XVI Región de Ñuble", "XVI Región de Ñuble")
)

class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    localidad = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.IntegerField()
    region = models.CharField(choices=REGION_CHOISES, max_length=200)
    
    class Meta:
        verbose_name_plural = 'Cliente'
        
    def __str__(self):
        return str(self.id)
    
# Modelo del Producto
CATEGORIA_CHOISES = (
    ("A", "Audifonos"),
    ("L", "Laptop"),
    ("M", "Mobiles"),
    ("T", "Teclados")
)

class Producto(models.Model):
    titulo = models.CharField(max_length=100)
    precio_venta = models.FloatField(validators=[MinValueValidator(1.0)])
    descripcion = models.TextField()
    marca = models.CharField(max_length=100)
    categoria = models.CharField(choices=CATEGORIA_CHOISES, max_length=50)
    imagen_producto = models.ImageField(upload_to='imagenproducto')
    
    class Meta:
        verbose_name_plural = 'Producto'
        
    def __str__(self):
        return str(self.id)
    
# Modelo del Carrito de Compras
class Carrito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name_plural = 'Carrito'
    
    def __str__(self):
        return str(self.id)
    
    @property
    def costo_total(self):
        return self.cantidad * self.producto.precio_venta
    
# Modelo del Pedido Realizado
ESTADO_CHOICES = (
    ('Aceptado', 'Aceptado'),
    ('Empacado', 'Empacado'),
    ('En camino', 'En camino'),
    ('Entregado', 'Entregado'),
    ('Cancelado', 'Cancelado')
)

class PedidoRealizado(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=100, default='Aceptado')
    precio_producto = models.FloatField(default=0)
    
    class Meta:
        verbose_name_plural = 'Pedido Realizado'
        
    def __str__(self):
        return str(self.id)
    
    @property
    def costo_total(self):
        return self.cantidad * self.precio_producto
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # Nuevo pedido, guardar el precio del producto actual
            self.precio_producto = self.producto.precio_venta
        super().save(*args, **kwargs)
    
    
# Modelo de Formulario de contacto

class FormularioContacto(models.Model):
    primer_nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    comentarios = models.TextField()
    correo_electronico = models.EmailField()
    ciudad = models.CharField(max_length= 100)


    