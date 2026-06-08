from django.db import models
from django.contrib.auth.models import User

DEPARTAMENTOS = [
    ('CALCULO', 'Cálculo de Material'),
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
    
    # === NUEVO: ROLES DE CÁLCULO ===
    ROLES_CALCULO = [
        ('MANO', 'Calculista Telar Manual'),
        ('MAQUINA', 'Calculista Máquina (Somet/Dornier)'),
        ('JEFE', 'Jefe / Administrador (Ve todo)'),
    ]
    rol_calculo = models.CharField(max_length=20, choices=ROLES_CALCULO, default='JEFE')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_calculo_display()}"

class OrdenTrabajo(models.Model):
    po_number = models.CharField(max_length=50, unique=True, verbose_name="P.O. Number")
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    cliente = models.CharField(max_length=150)
    diseno = models.CharField(max_length=150, verbose_name="Nombre del Diseño")
    
    ancho_ft = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Ancho (FT)")
    ancho_in = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Ancho (IN)")
    largo_ft = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Largo (FT)")
    largo_in = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Largo (IN)")
    
    TIPO_ALFOMBRA = [('MANO', 'A Mano'), ('MAQUINA', 'A Máquina')]
    tipo = models.CharField(max_length=10, choices=TIPO_ALFOMBRA)
    
    layout_img = models.ImageField(upload_to='layouts/', blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PO: {self.po_number} - {self.cliente}"

    @property
    def dimensiones(self):
        ancho = []
        if self.ancho_ft:
            ancho.append(f"{int(self.ancho_ft) if self.ancho_ft % 1 == 0 else self.ancho_ft}'")
        if self.ancho_in:
            ancho.append(f"{int(self.ancho_in) if self.ancho_in % 1 == 0 else self.ancho_in}\"")
        ancho_str = " ".join(ancho) or "0'"

        largo = []
        if self.largo_ft:
            largo.append(f"{int(self.largo_ft) if self.largo_ft % 1 == 0 else self.largo_ft}'")
        if self.largo_in:
            largo.append(f"{int(self.largo_in) if self.largo_in % 1 == 0 else self.largo_in}\"")
        largo_str = " ".join(largo) or "0'"

        return f"{ancho_str} x {largo_str}"
    
class InstruccionCorreo(models.Model):
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='instrucciones')
    fecha_recibido = models.DateField(verbose_name="Fecha del Correo")
    instrucciones_clave = models.TextField(verbose_name="Instrucciones Específicas")
    cuerpo_correo = models.TextField(verbose_name="Cuerpo Completo del Correo", blank=True, null=True)
    
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Instrucción {self.fecha_recibido} - PO: {self.orden.po_number}"

class TrackingProduccion(models.Model):
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='tracking')
    departamento = models.CharField(max_length=20, choices=DEPARTAMENTOS)
    
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(blank=True, null=True)
    
    ESTADOS = [('EN_PROCESO', 'En Proceso'), ('FINALIZADO', 'Finalizado')]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='EN_PROCESO')

    def __str__(self):
        return f"{self.orden.po_number} - {self.departamento} ({self.estado})"
    
class CalculoMaterial(models.Model):
    orden = models.OneToOneField(OrdenTrabajo, on_delete=models.CASCADE, related_name='calculo')
    
    TIPO_CALCULO = [('MANO', 'A Mano (Hand)'), ('MAQUINA', 'A Máquina (Machine)')]
    metodo = models.CharField(max_length=15, choices=TIPO_CALCULO)
    
    # === DATOS PARA TELAR MANUAL ===
    sq_ft = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, verbose_name="SQ.F.")
    hilos_por_pulgada = models.CharField(max_length=50, null=True, blank=True, verbose_name="Hilos x Plg")
    peine = models.CharField(max_length=50, null=True, blank=True, verbose_name="Peine")
    por_diente = models.CharField(max_length=100, null=True, blank=True, verbose_name="Por Diente")
    largo_urdir = models.CharField(max_length=50, null=True, blank=True, verbose_name="Largo Urdir") # NUEVO
    material_pie = models.TextField(verbose_name="Detalle Material en PIE", null=True, blank=True)
    material_trama = models.TextField(verbose_name="Detalle Material en TRAMA", null=True, blank=True)

    # === DATOS PARA TELAR MÁQUINA (SOMET) ===
    somet_yardas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Yardas SOMET")
    material_somet = models.TextField(verbose_name="Detalle Hilos SOMET", null=True, blank=True)
    
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # === DATOS PARA TELAR MÁQUINA (DORNIER) ===
    material_dornier = models.TextField(verbose_name="Detalle DORNIER JSON", null=True, blank=True)
    dornier_metros_urdir = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dornier_metros_lineales = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Cálculo {self.metodo} - PO: {self.orden.po_number}"