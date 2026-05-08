from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_principal, name='dashboard'),
    path('nueva-orden/', views.crear_orden, name='crear_orden'), # <-- Nueva ruta
    path('orden/<int:orden_id>/', views.ficha_orden, name='ficha_orden'),

    path('tineria/', views.panel_tineria, name='panel_tineria'), # <-- Nueva ruta para el panel de tinería  

    path('calculo/', views.panel_calculo, name='panel_calculo'), # <-- Nueva ruta para el panel de cálculo
    path('calculo/<int:orden_id>/', views.calcular_orden, name='calcular_orden'), # <-- Nueva ruta para la ficha de cálculo
]