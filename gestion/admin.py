from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models

from .forms import CustomUserCreationForm, CustomUserChangeForm, ProductoForm
from .models import CustomEmailUser, Producto, Pedido, DetallePedido
from .widgets import ImageWidget


# Register your models here.
@admin.register(CustomEmailUser)
class CustomEmailUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomEmailUser
    list_display = ('email', 'rut', 'nombre_completo', 'is_active', 'is_staff', 'is_superuser',)
    list_filter = ('email', 'rut', 'nombre_completo', 'is_active', 'is_staff', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'rut', 'nombre_completo', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser',
                'groups',
                'user_permissions')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    form = ProductoForm
    list_display = ('nombre', 'descripcion', 'precio', 'imagen')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha', 'numero_pedido', 'producto', 'estado', 'direccion_entrega', 'forma_pago')


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario')
