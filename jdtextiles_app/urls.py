from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_principal, name='dashboard'),
    path('nueva-orden/', views.crear_orden, name='crear_orden'), # <-- Nueva ruta
    path('orden/<int:orden_id>/', views.ficha_orden, name='ficha_orden'),
]