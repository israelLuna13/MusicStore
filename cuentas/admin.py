from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import FormCreacionUsuario, FormCambiarUsuario
from .models import UsuarioPers

class UsuarioAdmin(UserAdmin):
    add_form = FormCreacionUsuario
    form     = FormCambiarUsuario
    model    = UsuarioPers
    list_display = [
        'email',
        'username',
        'is_staff',
    ] 
        
# Register your models here.
admin.site.register(UsuarioPers,UsuarioAdmin)


