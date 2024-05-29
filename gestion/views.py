from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import HiddenInput

from .forms import CustomUserCreationForm, ChangeStatusForm, TakeOrderForm
from .models import Pedido, DetallePedido, CustomEmailUser


# Create your views here.
def home(request):
    return render(request, template_name='gestion/home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # genero una copia del formulario, ya que es inmutable por eso utilizo copy()
        form.data = form.data.copy()
        # accedo a los campos password 1 y 2 y les asigno una temporal para poder pasar la validacion
        # del form.is_valid()
        form.data['password1'] = settings.PASSWORD_TEMPORAL
        form.data['password2'] = settings.PASSWORD_TEMPORAL
        if form.is_valid():
            user = form.save(commit=False)
            temp_password = get_random_string(8)
            user.set_password(temp_password)
            user.save()
            send_mail(
                'Tu contraseña Temporal - Te Lo vendo',
                f'Hola {user.email}, aqui está tu contraseña temporal: {temp_password}\n Por favor cambia esta contraseña tras iniciar sesión por primera vez',
                'no-contestar@mailtrap.io',
                [user.email],
                fail_silently=False
            )
            return redirect('gestion:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'gestion/register.html', {'form': form})


class EmailLoginView(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('gestion:authenticated')
    template_name = 'gestion/login.html'


class EmailLogoutView(LogoutView):
    template_name = 'gestion/logout.html'
    next_page = 'gestion:logout'


@login_required(login_url='gestion:login')
def authenticated(request):
    if request.user.is_superuser or request.user.is_staff:
        pedidos_view = Pedido.objects.all()
        if pedidos_view.exists():
            return render(request, 'gestion/authenticated.html', context={'pedidos': pedidos_view})
        else:
            message = "No hay elementos que mostrar"
            return render(request, 'gestion/authenticated.html', context={'message': message})
    else:
        pedidos_view = Pedido.objects.filter(cliente_id=request.user.id)
        if pedidos_view.exists():
            return render(request, 'gestion/authenticated.html', context={'pedidos': pedidos_view})
        else:
            message = "No hay elementos que mostrar"
            return render(request, 'gestion/authenticated.html', context={'message': message})


@login_required(login_url='gestion:login')
def order_details(request, pedido_id):
    try:
        order_detail = DetallePedido.objects.get(pedido_id=pedido_id)
        return render(request, template_name='gestion/detail.html', context={'order_detail': order_detail})
    except DetallePedido.DoesNotExist:
        message = "No existe detalle del pedido"
        return render(request, 'gestion/detail.html', context={'message': message})


def order_status(request, pedido_id):
    order_details = get_object_or_404(Pedido, numero_pedido=pedido_id)
    if request.method == 'POST':
        change_status_form = ChangeStatusForm(request.POST, instance=order_details)
        if change_status_form.is_valid():
            change_status_form.save()
            send_mail(
                'Estado de envio - Te Lo vendo',
                f'Hola {order_details.cliente.nombre_completo}, su pedido a cambio de estado a {order_details.estado}',
                'no-contestar@mailtrap.io',
                [order_details.cliente.email],
                fail_silently=False
            )
            messages.success(request, "Estado del pedido cambiado correctamente.")
            return redirect('gestion:detail', pedido_id)
        else:
            messages.error(request, "No se ha podido guardar el estado")
    else:
        change_status_form = ChangeStatusForm(instance=order_details)

    return render(request, 'gestion/status.html', {'change_status_form': change_status_form})


def take_order(request):
    if request.method == 'POST':
        take_order_form = TakeOrderForm(request.POST)
        if take_order_form.is_valid():
            order = take_order_form.save(commit=False)
            if not request.user.is_superuser and not request.user.is_staff:
                order.cliente = request.user
            order.save()
            messages.success(request, "Pedido generado con éxito")
            return redirect('gestion:authenticated')
        else:
            messages.error(request, take_order_form.errors)
    else:
        take_order_form = TakeOrderForm(
            initial={'cliente': request.user if not request.user.is_superuser and not request.user.is_staff else None})

    return render(request, 'gestion/order.html', {
        'take_order_form': take_order_form,
        'is_superuser_or_staff': request.user.is_superuser or request.user.is_staff
    })


def delete_order(request, pedido_id):
    order = get_object_or_404(Pedido, numero_pedido=pedido_id)
    order.delete()
    messages.success(request, "Pedido eliminado correctamente.")
    return redirect('gestion:authenticated')
