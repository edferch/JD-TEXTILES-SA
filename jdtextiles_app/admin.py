from django.contrib import admin
from .models import OrdenTrabajo, InstruccionCorreo, TrackingProduccion, CalculoMaterial, PerfilUsuario
import json

admin.site.register(OrdenTrabajo)
admin.site.register(InstruccionCorreo)
admin.site.register(TrackingProduccion)
admin.site.register(PerfilUsuario)

@admin.register(CalculoMaterial)
class CalculoMaterialAdmin(admin.ModelAdmin):
    list_display = ('orden', 'metodo', 'creado_por', 'fecha_registro', 'ver_detalle')
    list_filter = ('metodo', 'fecha_registro')
    
    # Esta función transforma el texto feo en algo legible
    def ver_detalle(self, obj):
        if obj.metodo == 'MAQUINA':
            # Intentamos leer el JSON de Dornier
            try:
                data = json.loads(obj.material_dornier)
                # Retornamos un resumen rápido
                return f"Pie: {len(data.get('pie', []))} colores | Trama: {len(data.get('trama', []))} colores"
            except:
                return "Error en JSON"
        return "N/A"
    
    ver_detalle.short_description = "Detalle Técnico"