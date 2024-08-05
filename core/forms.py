from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Cliente, Producto
from django import forms
from .models import FormularioContacto

# Formulario de Registro del Cliente
class FormularioRegistroUsuario(UserCreationForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # Pone el orden en el que se mostraran en pantalla
        labels = {'email': 'email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya esta registrado. Intenta con otro')
        return username
        
# Formulario de Iniciar Sesion del Cliente
class FormularioLoginUsuario(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=("Contraseña"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    
# Formulario de Perfil del Cliente
class FormularioPerfilCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'localidad', 'ciudad', 'region', 'codigo_postal']
        widgets = {'nombre':forms.TextInput(attrs=
        {'class':'form-control'}), 'localidad':forms.TextInput(attrs=
        {'class':'form-control'}), 'ciudad':forms.TextInput(attrs=
        {'class':'form-control'}),
        'region':forms.Select(attrs={'class':'form-control'}),
        'codigo_postal':forms.NumberInput(attrs={'class':'form-control'})}

# Formulario de Contacto
class FormularioContacto (forms.ModelForm):
    class Meta:
        model = FormularioContacto
        fields = ['primer_nombre','apellidos','comentarios','correo_electronico','ciudad']
        
        def limpiar_correo(self):
            correo_electronico = self.cleaned_data ['correo_electronico']
            # Agregar regla de validación personalizada aca
            return correo_electronico
        
class ProductoForm(forms.ModelForm):
    
    class Meta:
        model = Producto
        fields = '__all__'