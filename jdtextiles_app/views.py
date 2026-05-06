from django.shortcuts import render, redirect
from .forms import OrdenTrabajoForm
from .models import OrdenTrabajo 

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