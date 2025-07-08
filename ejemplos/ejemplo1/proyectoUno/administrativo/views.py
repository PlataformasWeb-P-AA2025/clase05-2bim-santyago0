from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# importar las clases de models.py
from administrativo.models import *

# importar los formularios de forms.py
from administrativo.forms import *

# Create your views here.

def index(request):
    """
        Listar los registros del modelo Estudiante,
        obtenidos de la base de datos.
    """
    # a través del ORM de django se obtiene
    # los registros de la entidad; el listado obtenido
    # se lo almacena en una variable llamada
    # estudiantes
    estudiantes = Estudiante.objects.all()
    # en la variable tipo diccionario llamada informacion_template
    # se agregará la información que estará disponible
    # en el template
    informacion_template = {'estudiantes': estudiantes, 'numero_estudiantes': len(estudiantes)}
    return render(request, 'index.html', informacion_template)

def ingreso(request):

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.data.get("username")
            raw_password = form.data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect(index)
    else:
        form = AuthenticationForm()

    informacion_template = {'form': form}
    return render(request, 'registration/login.html', informacion_template)

def logout_view(request):
    logout(request)
    messages.info(request, "Has salido del sistema")
    return redirect(index)

@login_required
@permission_required('administrativo.view_estudiante')
def obtener_estudiante(request, id):
    """
        Listar los registros del modelo Estudiante,
        obtenidos de la base de datos.
    """
    # a través del ORM de django se obtiene
    # los registros de la entidad; el listado obtenido
    # se lo almacena en una variable llamada
    # estudiantes
    estudiante = Estudiante.objects.get(pk=id)
    # en la variable tipo diccionario llamada informacion_template
    # se agregará la información que estará disponible
    # en el template
    informacion_template = {'estudiante': estudiante}
    return render(request, 'obtener_estudiante.html', informacion_template)


# @login_required(login_url='/entrando/login/')
@login_required
@permission_required('administrativo.add_estudiante', )
# @permission_required('administrativo.add_estudiante', login_url="/entrando/login/")
def crear_estudiante(request):
    """
    """
    if request.method=='POST':
        formulario = EstudianteForm(request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save() # se guarda en la base de datos
            return redirect(index)
    else:
        formulario = EstudianteForm()
    diccionario = {'formulario': formulario}

    return render(request, 'crearEstudiante.html', diccionario)


@login_required # (login_url='/entrando/login/')
@permission_required('administrativo.change_estudiante',)
def editar_estudiante(request, id):
    """
    """
    estudiante = Estudiante.objects.get(pk=id)
    if request.method=='POST':
        formulario = EstudianteForm(request.POST, instance=estudiante)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = EstudianteForm(instance=estudiante)
    diccionario = {'formulario': formulario}

    return render(request, 'editarEstudiante.html', diccionario)


@login_required
@permission_required('administrativo.delete_estudiante')
def eliminar_estudiante(request, id):
    """
    """
    estudiante = Estudiante.objects.get(pk=id)
    estudiante.delete()
    return redirect(index)

# atención para permitir que una función sea usada por
# un grupo específico
def en_grupo(nombre):
    def predicate(user):
        return user.groups.filter(name=nombre).exists()
    return user_passes_test(predicate)

@en_grupo('supervisor')
@login_required
@permission_required('administrativo.add_numero_telefonico')
def crear_numero_telefonico(request):
    """
    """

    if request.method=='POST':
        formulario = NumeroTelefonicoForm(request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = NumeroTelefonicoForm()
    diccionario = {'formulario': formulario}

    return render(request, 'crearNumeroTelefonico.html', diccionario)


@login_required
@permission_required('administrativo.change_numero_telefonico')
def editar_numero_telefonico(request, id):
    """
    """
    telefono = NumeroTelefonico.objects.get(pk=id)
    if request.method=='POST':
        formulario = NumeroTelefonicoForm(request.POST, instance=telefono)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = NumeroTelefonicoForm(instance=telefono)
    diccionario = {'formulario': formulario}

    return render(request, 'crearNumeroTelefonico.html', diccionario)

@login_required
@permission_required('administrativo.add_numero_telefonico')
def crear_numero_telefonico_estudiante(request, id):
    """
    """
    estudiante = Estudiante.objects.get(pk=id)
    if request.method=='POST':
        formulario = NumeroTelefonicoEstudianteForm(estudiante, request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = NumeroTelefonicoEstudianteForm(estudiante)
    diccionario = {'formulario': formulario, 'estudiante': estudiante}

    return render(request, 'crearNumeroTelefonicoEstudiante.html', diccionario)

"""
Descripción en Admin	      codename
Can add Estudiante	          add_estudiante
Can change Estudiante	      change_estudiante
Can delete Estudiante	      delete_estudiante
Can view Estudiante	          view_estudiante
"""
