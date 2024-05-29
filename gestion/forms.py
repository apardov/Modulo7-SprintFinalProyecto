from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, ModelChoiceField
from django import forms
from .models import CustomEmailUser, Pedido, DetallePedido, Producto


# definicion de formularios para creacion de usuarios y modificacion de estos
# usando los predefinidos que Django provee
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomEmailUser
        fields = ('email', 'rut', 'nombre_completo')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomEmailUser
        fields = ('email', 'rut', 'nombre_completo')


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'


class DetallePedidoForm(ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'


class ChangeStatusForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']


class TakeOrderForm(ModelForm):
    cliente = ModelChoiceField(queryset=CustomEmailUser.objects.all())

    class Meta:
        model = Pedido
        fields = ['cliente', 'numero_pedido', 'direccion_entrega', 'forma_pago', 'producto']


class ProductoForm(forms.ModelForm):
    imagen_file = forms.FileField(required=False)

    class Meta:
        model = Producto
        exclude = ('imagen',)

    def save(self, commit=True):
        producto = super().save(commit=False)
        imagen_file = self.cleaned_data.get('imagen_file')

        if imagen_file:
            with imagen_file.open('rb') as file:
                producto.imagen = file.read()

        if commit:
            producto.save()

        return producto
