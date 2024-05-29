from django.urls import path
from .views import register, EmailLoginView, EmailLogoutView, authenticated, home, order_details, order_status, \
    take_order, delete_order

app_name = 'gestion'

urlpatterns = [
    path('', home, name='home'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', EmailLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('authenticated/', authenticated, name='authenticated'),
    path('detail/<int:pedido_id>', order_details, name='detail'),
    path('status/<int:pedido_id>', order_status, name='status'),
    path('order/', take_order, name='order'),
    path('delete/<int:pedido_id>', delete_order, name='delete'),
]
