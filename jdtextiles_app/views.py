from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrdenTrabajoForm, InstruccionForm
from .models import OrdenTrabajo, InstruccionCorreo

def dashboard_principal(request):
    #Traer ordenes de PostgreSQL
    ordenes = OrdenTrabajo.objects.all().order_by('-fecha_creacion') # Ordenamos por fecha de creación, la más reciente primero

    #se envia a la plantilla HTML
    return render(request, 'index.html', {'ordenes': ordenes})

def crear_orden(request):
    # Si el usuario le dio clic al botón "Guardar" (POST)
    if request.method == 'POST':
        # Recibimos los datos de texto y los archivos (la imagen del layout)
        form = OrdenTrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # ¡Aquí se guarda mágicamente en PostgreSQL!
            return redirect('dashboard') # Lo regresamos a la pantalla principal
    else:
        # Si solo está entrando a ver la página, le mostramos el formulario vacío
        form = OrdenTrabajoForm()
    
    return render(request, 'crear_orden.html', {'form': form})

def ficha_orden(request, orden_id):
    # Buscamos la orden específica en la base de datos
    orden = get_object_or_404(OrdenTrabajo, id=orden_id)
    
    # Traemos todas las instrucciones que ya tiene esta orden
    instrucciones = orden.instrucciones.all().order_by('-fecha_registro')
    
    # Si el usuario quiere guardar un nuevo correo
    if request.method == 'POST':
        form = InstruccionForm(request.POST)
        if form.is_valid():
            nueva_instruccion = form.save(commit=False)
            nueva_instruccion.orden = orden # Amarramos la instrucción a esta orden
            nueva_instruccion.creado_por = request.user # Guardamos quién lo hizo
            nueva_instruccion.save()
            return redirect('ficha_orden', orden_id=orden.id) # Recargamos la página
    else:
        form = InstruccionForm()
        
    return render(request, 'ficha_orden.html', {
        'orden': orden,
        'instrucciones': instrucciones,
        'form': form
    })