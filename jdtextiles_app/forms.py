from django import forms
from .models import OrdenTrabajo, InstruccionCorreo, CalculoMaterial

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        # Qué campos le pediremos al usuario que llene
        fields = ['po_number', 'invoice_number', 'cliente', 'diseno', 'dimensiones', 'tipo', 'layout_img']
        
        input_classes = 'w-full p-2.5 bg-white text-slate-800 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition-all'
        
        # Le inyectamos los estilos de Tailwind a cada cajita de texto
        widgets = {
            'po_number': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'invoice_number': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'cliente': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'diseno': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'dimensiones': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'tipo': forms.Select(attrs={'class': input_classes}),
            'layout_img': forms.FileInput(attrs={'class': 'w-full p-2 bg-white text-slate-800 border border-slate-300 rounded-md shadow-sm'}),
        }

class InstruccionForm(forms.ModelForm):
    class Meta:
        model = InstruccionCorreo
        fields = ['fecha_recibido', 'instrucciones_clave', 'cuerpo_correo'] # Agregamos ambos
        
        input_classes = 'w-full p-2.5 bg-white text-slate-800 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition-all'
        
        widgets = {
            'fecha_recibido': forms.DateInput(attrs={'type': 'date', 'class': input_classes, 'autocomplete': 'off'}),
            'instrucciones_clave': forms.Textarea(attrs={'class': input_classes + ' mb-2', 'rows': 3, 'placeholder': '¿Qué hay que hacer exactamente?'}),
            'cuerpo_correo': forms.Textarea(attrs={'class': input_classes, 'rows': 5, 'placeholder': 'Pega aquí todo el texto del correo...'}),
        }
class CalculoMaterialForm(forms.ModelForm):
    class Meta:
        model = CalculoMaterial
        fields = ['metodo', 'sq_ft', 'hilos_por_pulgada', 'peine', 'por_diente', 'material_pie', 'material_trama']
        
        input_classes = 'w-full p-2.5 bg-white text-slate-800 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition-all'
        
        widgets = {
            'metodo': forms.Select(attrs={'class': 'w-full p-3 bg-white text-slate-800 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 font-bold transition-all', 'id': 'select-metodo'}),
            'sq_ft': forms.NumberInput(attrs={'class': input_classes, 'step': '0.001', 'autocomplete': 'off'}),
            'hilos_por_pulgada': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'peine': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'por_diente': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            
            # Textareas para los desgloses de colores y libras
            'material_pie': forms.Textarea(attrs={'class': 'w-full p-3 bg-slate-50 text-slate-800 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 font-mono text-sm transition-all', 'rows': 5, 'placeholder': 'Ej. SDA 34/2 - pendine sands - 5/u T...'}),
            'material_trama': forms.Textarea(attrs={'class': 'w-full p-3 bg-slate-50 text-slate-800 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 font-mono text-sm transition-all', 'rows': 5, 'placeholder': 'Ej. Fino SDA 34/2 - pendine sands - 5/u...'}),
        }