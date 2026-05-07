from django.db import models
from django.contrib.auth.models import User

# Opciones de departamentos para el filtrado (El inicio de nuestro RBAC)
DEPARTAMENTOS = [
    ('BODEGA', 'Bodega'),
    ('TINERIA', 'Tiñería'),
    ('PREPARACION', 'Preparación'),
    ('TELAR', 'Telar/Tejido'),
    ('TERMINADOS', 'Terminados'),
    ('GERENCIA', 'Gerencia'),
]

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    departamento = models.CharField(max_length=20, choices=DEPARTAMENTOS)

    def __str__(self):
        return f"{self.usuario.username} - {self.departamento}"

class OrdenTrabajo(models.Model):
    po_number = models.CharField(max_length=50, unique=True, verbose_name="P.O. Number")
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    cliente = models.CharField(max_length=150)
    diseno = models.CharField(max_length=150, verbose_name="Nombre del Diseño")
    dimensiones = models.CharField(max_length=100, verbose_name="Size (Width x Length)")
    
    TIPO_ALFOMBRA = [('MANO', 'A Mano'), ('MAQUINA', 'A Máquina')]
    tipo = models.CharField(max_length=10, choices=TIPO_ALFOMBRA)
    
    layout_img = models.ImageField(upload_to='layouts/', blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PO: {self.po_number} - {self.cliente}"
    
class InstruccionCorreo(models.Model):
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='instrucciones')
    fecha_recibido = models.DateField(verbose_name="Fecha del Correo")
    # Instrucciones resumidas para los operarios
    instrucciones_clave = models.TextField(verbose_name="Instrucciones Específicas")
    # El correo completo como respaldo
    cuerpo_correo = models.TextField(verbose_name="Cuerpo Completo del Correo", blank=True, null=True)
    
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Instrucción {self.fecha_recibido} - PO: {self.orden.po_number}"

class TrackingProduccion(models.Model):
    # Esta tabla reemplaza el Spreadsheet de Excel
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='tracking')
    departamento = models.CharField(max_length=20, choices=DEPARTAMENTOS)
    
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(blank=True, null=True)
    
    ESTADOS = [('EN_PROCESO', 'En Proceso'), ('FINALIZADO', 'Finalizado')]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='EN_PROCESO')

    def __str__(self):
        return f"{self.orden.po_number} - {self.departamento} ({self.estado})"