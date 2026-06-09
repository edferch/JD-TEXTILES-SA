from django.contrib import admin
from .models import OrdenTrabajo, InstruccionCorreo, TrackingProduccion, CalculoMaterial, PerfilUsuario
import json
from django.utils.safestring import mark_safe

admin.site.register(OrdenTrabajo)
admin.site.register(InstruccionCorreo)
admin.site.register(TrackingProduccion)
admin.site.register(PerfilUsuario)

@admin.register(CalculoMaterial)
class CalculoMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'orden', 'metodo', 'creado_por', 'fecha_registro', 
        'sq_ft', 'peine', 'hilos_por_pulgada', 'por_diente', 'largo_urdir',
        'somet_yardas', 'dornier_metros_urdir', 'dornier_metros_lineales'
    )
    list_filter = ('metodo', 'fecha_registro')
    search_fields = ('orden__po_number', 'orden__cliente')
    
    fieldsets = (
        ('Información General', {
            'fields': ('orden', 'metodo', 'creado_por', 'fecha_registro')
        }),
        ('Datos: Telar Manual', {
            'fields': ('sq_ft', 'hilos_por_pulgada', 'peine', 'por_diente', 'largo_urdir', 'detalle_pie', 'detalle_trama')
        }),
        ('Datos: Telar Máquina (Somet)', {
            'fields': ('somet_yardas', 'detalle_somet')
        }),
        ('Datos: Telar Máquina (Dornier)', {
            'fields': ('dornier_metros_urdir', 'dornier_metros_lineales', 'detalle_dornier')
        }),
    )
    readonly_fields = ('fecha_registro', 'detalle_pie', 'detalle_trama', 'detalle_somet', 'detalle_dornier')

    # --- FUNCIONES PARA FORMATEAR EL JSON EN TABLAS VISUALES ---
    def detalle_pie(self, obj):
        return self.formatear_json(obj.material_pie)
    detalle_pie.short_description = "Material PIE (Detalle)"

    def detalle_trama(self, obj):
        return self.formatear_json(obj.material_trama)
    detalle_trama.short_description = "Material TRAMA (Detalle)"

    def detalle_somet(self, obj):
        return self.formatear_json(obj.material_somet)
    detalle_somet.short_description = "Material SOMET (Detalle)"

    def detalle_dornier(self, obj):
        return self.formatear_json(obj.material_dornier)
    detalle_dornier.short_description = "Material DORNIER (Detalle)"

    def formatear_json(self, valor_json):
        if not valor_json or valor_json in ['[]', '{}']:
            return "Sin datos registrados"
        try:
            data = json.loads(valor_json)
            
            # Si es un diccionario (Caso particular de Telar Dornier que tiene nm_universal, pie y trama)
            if isinstance(data, dict):
                html = f"<div style='margin-bottom: 10px; font-size: 14px;'><strong>No. Métrico Universal:</strong> {data.get('nm_universal', 'N/A')}</div>"
                if data.get('pie'):
                    html += "<div style='margin-top:10px; font-weight:bold; color:#1e40af;'>HILOS DE PIE:</div>" + self.generar_tabla_html(data.get('pie', []))
                if data.get('trama'):
                    html += "<div style='margin-top:10px; font-weight:bold; color:#9a3412;'>HILOS DE TRAMA:</div>" + self.generar_tabla_html(data.get('trama', []))
                return mark_safe(html)
            
            # Si es una lista (Caso Somet, y telar Manual)
            elif isinstance(data, list):
                return mark_safe(self.generar_tabla_html(data))
            
            return valor_json
        except Exception:
            # Si falla, mostramos el formato original con corchetes
            return valor_json

    def generar_tabla_html(self, lista_datos):
        if not lista_datos or not isinstance(lista_datos, list):
            return "<p style='color: gray;'>Sin datos registrados</p>"
        
        # Obtenemos las cabeceras (títulos de columnas) del primer elemento
        cabeceras = lista_datos[0].keys()
        
        # Creamos una estructura HTML estilizada
        html = '<table style="width: 100%; border-collapse: collapse; text-align: left; margin-top: 5px; margin-bottom: 15px; font-size: 13px; font-family: Arial, sans-serif; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">'
        html += '<thead style="background-color: #f1f5f9; color: #334155;"><tr>'
        for cabecera in cabeceras:
            # Limpiamos el texto de las cabeceras, por ejemplo de 'lbs_final' a 'LBS FINAL'
            titulo = str(cabecera).replace("_", " ").upper()
            html += f'<th style="border: 1px solid #cbd5e1; padding: 10px; font-weight: bold;">{titulo}</th>'
        html += '</tr></thead><tbody>'
        
        # Llenamos las filas con los datos correspondientes
        for fila in lista_datos:
            html += '<tr style="background-color: #ffffff; transition: background-color 0.2s;">'
            for cabecera in cabeceras:
                valor = fila.get(cabecera, '')
                html += f'<td style="border: 1px solid #e2e8f0; padding: 10px; color: #475569;">{valor}</td>'
            html += '</tr>'
        html += '</tbody></table>'
        
        return html