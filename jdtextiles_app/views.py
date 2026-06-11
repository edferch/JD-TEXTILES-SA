import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrdenTrabajoForm, InstruccionForm, CalculoMaterialForm
from .models import OrdenTrabajo, InstruccionCorreo, CalculoMaterial, PerfilUsuario

@login_required(login_url='login')
def dashboard_principal(request):
    ordenes = OrdenTrabajo.objects.all().order_by('-fecha_creacion')
    return render(request, 'index.html', {'ordenes': ordenes})

@login_required(login_url='login')
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = OrdenTrabajoForm()
    
    return render(request, 'crear_orden.html', {'form': form})

@login_required(login_url='login')
def ficha_orden(request, orden_id):
    orden = get_object_or_404(OrdenTrabajo, id=orden_id)
    instrucciones = orden.instrucciones.all().order_by('-fecha_registro')
    
    if request.method == 'POST':
        form = InstruccionForm(request.POST)
        if form.is_valid():
            nueva_instruccion = form.save(commit=False)
            nueva_instruccion.orden = orden
            nueva_instruccion.creado_por = request.user
            nueva_instruccion.save()
            return redirect('ficha_orden', orden_id=orden.id)
    else:
        form = InstruccionForm()
        
    return render(request, 'ficha_orden.html', {
        'orden': orden,
        'instrucciones': instrucciones,
        'form': form
    })

@login_required(login_url='login')
def panel_tineria(request):
    ordenes = OrdenTrabajo.objects.all().order_by('-fecha_creacion')
    return render(request, 'panel_tineria.html', {'ordenes': ordenes})

@login_required(login_url='login')
def panel_calculo(request):
    try:
        perfil = request.user.perfilusuario
    except PerfilUsuario.DoesNotExist:
        # Si no tiene perfil, le mostramos vacío por seguridad
        return render(request, 'panel_calculo.html', {'ordenes': []})

    # Filtramos las órdenes que NO tienen cálculo (isnull=True) Y según el rol
    ordenes_pendientes = OrdenTrabajo.objects.filter(calculo__isnull=True).order_by('fecha_creacion')

    if perfil.rol_calculo == 'MANO':
        ordenes_pendientes = ordenes_pendientes.filter(tipo='MANO')
    elif perfil.rol_calculo == 'MAQUINA':
        ordenes_pendientes = ordenes_pendientes.filter(tipo='MAQUINA')

    return render(request, 'panel_calculo.html', {'ordenes': ordenes_pendientes})

@login_required(login_url='login')
def calcular_orden(request, orden_id):
    orden = get_object_or_404(OrdenTrabajo, id=orden_id)
    
    # Buscamos si ya existe un cálculo previo para editarlo
    try:
        calculo = CalculoMaterial.objects.get(orden=orden)
    except CalculoMaterial.DoesNotExist:
        calculo = None

    if request.method == 'POST':
        form = CalculoMaterialForm(request.POST, instance=calculo)
        if form.is_valid():
            calculo_obj = form.save(commit=False)
            calculo_obj.orden = orden
            calculo_obj.creado_por = request.user
            calculo_obj.save()
            return redirect('panel_calculo')
    else:
        form = CalculoMaterialForm(instance=calculo)
        
    return render(request, 'calcular_orden.html', {'orden': orden, 'form': form})