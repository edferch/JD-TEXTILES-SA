from django.contrib import admin
from .models import OrdenTrabajo, PerfilUsuario, InstruccionCorreo, TrackingProduccion

admin.site.register(OrdenTrabajo)
admin.site.register(PerfilUsuario)
admin.site.register(InstruccionCorreo)
admin.site.register(TrackingProduccion)

admin.site.site_header = "Administración - JD Textiles SA"
admin.site.index_title = "Panel de Control de Producción"