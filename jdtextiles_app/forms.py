from django import forms
from .models import OrdenTrabajo

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        # Qué campos le pediremos al usuario que llene
        fields = ['po_number', 'invoice_number', 'cliente', 'diseno', 'dimensiones', 'tipo', 'layout_img']
        
        # Le inyectamos los estilos de Tailwind a cada cajita de texto
        widgets = {
            'po_number': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500'}),
            'invoice_number': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500'}),
            'cliente': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500'}),
            'diseno': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500'}),
            'dimensiones': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500'}),
            'tipo': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500'}),
            'layout_img': forms.FileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
        }