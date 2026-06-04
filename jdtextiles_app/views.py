from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required   #importa el candado
from .forms import OrdenTrabajoForm, InstruccionForm, CalculoMaterialForm
from .models import OrdenTrabajo, InstruccionCorreo

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrdenTrabajo, CalculoMaterial

@login_required(login_url='login')  # Esto asegura que solo los usuarios logueados puedan ver esta vista
def dashboard_principal(request):
    #Traer ordenes de PostgreSQL
    ordenes = OrdenTrabajo.objects.all().order_by('-fecha_creacion') # Ordenamos por fecha de creación, la más reciente primero

    #se envia a la plantilla HTML
    return render(request, 'index.html', {'ordenes': ordenes})

@login_required(login_url='login')
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


@login_required(login_url='login')
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

@login_required(login_url='login')
def panel_tineria(request):
    #Traer las ordenes
    ordenes = OrdenTrabajo.objects.all().order_by('-fecha_creacion') # Ordenamos por fecha de creación, la más reciente primero
    
    return render(request, 'panel_tineria.html', {'ordenes': ordenes})

@login_required(login_url='login')
def panel_calculo(request):
    # Magia de Django: Filtramos SOLO las órdenes que NO tienen cálculo (isnull=True)
    ordenes_pendientes = OrdenTrabajo.objects.filter(calculo__isnull=True).order_by('fecha_creacion')
    return render(request, 'panel_calculo.html', {'ordenes': ordenes_pendientes})

@login_required(login_url='login')
def calcular_orden(request, orden_id):
    orden = get_object_or_404(OrdenTrabajo, id=orden_id)
    
    if request.method == 'POST':
        # 1. Obtenemos las cajas de texto estáticas usando el atributo 'name'
        peine = request.POST.get('peine', '')
        hilos_plg = request.POST.get('hilos_plg', '')
        por_pua = request.POST.get('por_pua', '')
        sq_ft = request.POST.get('hidden_sq_ft', '0')
        
        # 2. Obtenemos todas las filas dinámicas de Pie y Trama empaquetadas en JSON
        datos_pie = request.POST.get('datos_pie_json', '[]')
        datos_trama = request.POST.get('datos_trama_json', '[]')
        
        # 3. Guardamos o actualizamos la base de datos
        calculo, creado = CalculoMaterial.objects.get_or_create(orden=orden)
        calculo.metodo = 'MANO'
        calculo.peine = peine
        calculo.hilos_por_pulgada = hilos_plg
        calculo.por_diente = por_pua
        calculo.sq_ft = sq_ft
        calculo.material_pie = datos_pie     # Se guarda como texto JSON
        calculo.material_trama = datos_trama # Se guarda como texto JSON
        calculo.creado_por = request.user
        calculo.save()
        
        # Redirigir al calculista a su bandeja de entrada
        return redirect('panel_calculo')
        
    return render(request, 'calcular_orden.html', {'orden': orden})