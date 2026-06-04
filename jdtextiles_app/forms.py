import re
from django import forms
from .models import OrdenTrabajo, InstruccionCorreo, CalculoMaterial

def parse_dimensiones(valor):
    if not valor:
        return 0, 0
    # Buscar pies (ej. 9', 9.5', o con comillas inteligentes del celular)
    ft_match = re.search(r'(\d+(?:\.\d+)?)\s*[\'’‘]', valor)
    # Buscar pulgadas (ej. 3", 3.5", o 3'')
    in_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:"|”|“|\'\'|’’|‘‘)', valor)
    
    ft = float(ft_match.group(1)) if ft_match else 0.0
    inch = float(in_match.group(1)) if in_match else 0.0
    
    # Si el usuario solo escribió números (ej. "9"), asumimos que son pies
    if not ft_match and not in_match:
        try:
            ft = float(valor.strip())
        except ValueError:
            pass
            
    return ft, inch

class OrdenTrabajoForm(forms.ModelForm):
    # Campos virtuales para facilitar el ingreso de datos
    ancho_input = forms.CharField(
        label="Ancho (ej: 9' 3\")", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'w-full p-2.5 bg-white text-slate-800 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition-all', 'autocomplete': 'off', 'placeholder': 'Ej: 9\' 3"'})
    )
    largo_input = forms.CharField(
        label="Largo (ej: 12' 6\")", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'w-full p-2.5 bg-white text-slate-800 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition-all', 'autocomplete': 'off', 'placeholder': 'Ej: 12\' 6"'})
    )

    class Meta:
        model = OrdenTrabajo
        # Reemplazamos los 4 campos originales de dimensiones por los 2 virtuales
        fields = ['po_number', 'invoice_number', 'cliente', 'diseno', 'ancho_input', 'largo_input', 'tipo', 'layout_img']
        
        input_classes = 'w-full p-2.5 bg-white text-slate-800 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition-all'
        
        # Le inyectamos los estilos de Tailwind a cada cajita de texto
        widgets = {
            'po_number': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'invoice_number': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'cliente': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'diseno': forms.TextInput(attrs={'class': input_classes, 'autocomplete': 'off'}),
            'tipo': forms.Select(attrs={'class': input_classes}),
            'layout_img': forms.FileInput(attrs={'class': 'w-full p-2 bg-white text-slate-800 border border-slate-300 rounded-md shadow-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando una orden existente, precargamos los campos visuales
        if self.instance and self.instance.pk:
            ancho_str = []
            # Eliminamos los decimales innecesarios (ej. 9.0 -> 9) al mostrar
            if self.instance.ancho_ft: ancho_str.append(f"{int(self.instance.ancho_ft) if self.instance.ancho_ft % 1 == 0 else self.instance.ancho_ft}'")
            if self.instance.ancho_in: ancho_str.append(f"{int(self.instance.ancho_in) if self.instance.ancho_in % 1 == 0 else self.instance.ancho_in}\"")
            self.fields['ancho_input'].initial = " ".join(ancho_str) or "0'"

            largo_str = []
            if self.instance.largo_ft: largo_str.append(f"{int(self.instance.largo_ft) if self.instance.largo_ft % 1 == 0 else self.instance.largo_ft}'")
            if self.instance.largo_in: largo_str.append(f"{int(self.instance.largo_in) if self.instance.largo_in % 1 == 0 else self.instance.largo_in}\"")
            self.fields['largo_input'].initial = " ".join(largo_str) or "0'"

    def clean(self):
        cleaned_data = super().clean()
        ancho_str = cleaned_data.get('ancho_input', '')
        largo_str = cleaned_data.get('largo_input', '')

        # Extraemos pies y pulgadas con nuestra función de expresiones regulares
        ancho_ft, ancho_in = parse_dimensiones(ancho_str)
        largo_ft, largo_in = parse_dimensiones(largo_str)

        # Los guardamos temporalmente en cleaned_data para usarlos en el save()
        cleaned_data['ancho_ft'] = ancho_ft
        cleaned_data['ancho_in'] = ancho_in
        cleaned_data['largo_ft'] = largo_ft
        cleaned_data['largo_in'] = largo_in

        return cleaned_data

    def save(self, commit=True):
        # Obtenemos la instancia del modelo antes de guardar
        instance = super().save(commit=False)
        
        # Asignamos los valores separados en sus respectivas columnas de la base de datos
        instance.ancho_ft = self.cleaned_data.get('ancho_ft', 0)
        instance.ancho_in = self.cleaned_data.get('ancho_in', 0)
        instance.largo_ft = self.cleaned_data.get('largo_ft', 0)
        instance.largo_in = self.cleaned_data.get('largo_in', 0)
        
        if commit:
            instance.save()
        return instance

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