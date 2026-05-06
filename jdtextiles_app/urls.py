from django.urls import path
from . import views

urlpatterns = [
    # Cuando la ruta esté vacía (es decir, la página principal), ejecuta la vista del dashboard
    path('', views.dashboard_principal, name='dashboard'),
]