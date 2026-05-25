from django import forms
from .models import OrdenTrabajo, InstruccionCorreo, CalculoMaterial

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        # Qué campos le pediremos al usuario que llene
        fields = ['po_number', 'invoice_number', 'cliente', 'diseno', 'dimensiones', 'tipo', 'layout_img']
        
        # Le inyectamos los estilos de Tailwind a cada cajita de texto
        widgets = {
            'po_number': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500', 'autocomplete': 'off'}),
            'invoice_number': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500', 'autocomplete': 'off'}),
            'cliente': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500', 'autocomplete': 'off'}),
            'diseno': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500', 'autocomplete': 'off'}),
            'dimensiones': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500', 'autocomplete': 'off'}),
            'tipo': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500'}),
            'layout_img': forms.FileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
        }

class InstruccionForm(forms.ModelForm):
    class Meta:
        model = InstruccionCorreo
        fields = ['fecha_recibido', 'instrucciones_clave', 'cuerpo_correo'] # Agregamos ambos
        
        widgets = {
            'fecha_recibido': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border border-gray-300 rounded focus:border-blue-500', 'autocomplete': 'off'}),
            'instrucciones_clave': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded mb-2', 'rows': 3, 'placeholder': '¿Qué hay que hacer exactamente?'}),
            'cuerpo_correo': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'rows': 5, 'placeholder': 'Pega aquí todo el texto del correo...'}),
        }
class CalculoMaterialForm(forms.ModelForm):
    class Meta:
        model = CalculoMaterial
        fields = ['metodo', 'sq_ft', 'hilos_por_pulgada', 'peine', 'por_diente', 'material_pie', 'material_trama']
        
        widgets = {
            'metodo': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg bg-gray-50 focus:border-blue-500 font-bold', 'id': 'select-metodo'}),
            'sq_ft': forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:border-blue-500', 'step': '0.001', 'autocomplete': 'off'}),
            'hilos_por_pulgada': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:border-blue-500', 'autocomplete': 'off'}),
            'peine': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:border-blue-500', 'autocomplete': 'off'}),
            'por_diente': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:border-blue-500', 'autocomplete': 'off'}),
            
            # Textareas para los desgloses de colores y libras
            'material_pie': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg font-mono text-sm', 'rows': 5, 'placeholder': 'Ej. SDA 34/2 - pendine sands - 5/u T...'}),
            'material_trama': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg font-mono text-sm', 'rows': 5, 'placeholder': 'Ej. Fino SDA 34/2 - pendine sands - 5/u...'}),
        }