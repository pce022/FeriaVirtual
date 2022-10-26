from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from app.models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from datetime import datetime

#permisos
from rolepermissions.roles import assign_role, remove_role
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required 
from rolepermissions.decorators import has_role_decorator
from rolepermissions.decorators import has_permission_decorator
#rest_framework
from rest_framework import viewsets 
from .serializers import ProductoSerializars
#xhtml2pdf
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
#email
from django.core.mail import send_mail


# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def index(request):
    return render(request, 'app/index.html')


def register(request):

    data = {'form': CustomUserCreationFrom()}
    if request.method == 'POST':
        formulario = CustomUserCreationFrom(data=request.POST)
        
        if formulario.is_valid():
            
            formulario.save()
            user = authenticate(username = formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"] )
            assign_role(user, 'entrada')
            assign_role(user, 'moderador') 
            login(request, user) 
            messages.success(request, "Registro completo, complete el siguiente formulario para terminar su registro")
            return redirect(to="create_staff")
        data["form"] = formulario    
    
    return render(request, 'registration/register.html',data)


def message_register(request):

    if request.method == 'POST':

        from_personal = message_register_t(request.POST, request.FILES)
       
        if from_personal.is_valid():
            instance = from_personal.save(commit=False)
            
            instance.save()
            messages.success(request, "Solicitud de registro enviado correctamente")
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            email = request.POST.get('email_mensaje')
            rut = request.POST.get('rut_personal')
            telefono = request.POST.get('movil_personal')
            pais_mensaje = request.POST.get('pais_personal')
            cuidad = request.POST.get('cuidad_personal')
            direccion = request.POST.get('direccion_personal')
            profesion = request.POST.get('profesion_personal')
            genero = request.POST.get('sexo_personal')
            mensaje = request.POST.get('mensaje')
            TipoPersonal = request.POST.get('tipo_personal_fk')

            
            subcjet = nombre #Nombre del contacto  
            message="Solicitud de registro de " + nombre +" "+ apellido + "\nDatos de la solicitud:\nNombre "+  nombre + " \nApellido: " + apellido + "\nEmail: " + email + "\nRut: " + rut + "\nTelefono: " + telefono + "\nPais: " + pais_mensaje + "\nCuidad: " + cuidad + "\nDireccion: " + direccion + "\nProfesion: " + profesion + "\nGenero: " + genero + "\nTipo Personal: "+ TipoPersonal + "\nMensaje: " + mensaje
            from_email = settings.EMAIL_HOST_USER #Email maipo grande
            recipient_list = [settings.EMAIL_HOST_USER]#Email a enviar el correo
            send_mail(subcjet, message, from_email, recipient_list)
            
            return redirect(message_register)

    else:
        from_personal = message_register_t 

    return  render(request, 'app/message_register.html',{'formulario' :from_personal})    

def create_user(request):

    usuarios = Usuario.objects.order_by('id')
    if request.method == 'GET': 

        form_usuario = UsuariolFrom()
      
    else:
        form_usuario = UsuariolFrom(request.POST)

        if  form_usuario.is_valid():

            form_usuario.save()
            return redirect('/create_user')

    return  render(request, 'app/create_user.html',{'form_usuario':form_usuario, 'usuarios':usuarios }   )


def list_user(request):
    usuario = Usuario.objects.order_by('-id')
    contexto = {'usuario':usuario}

    return  render(request, 'app/list_user.html',contexto)

    
def delete_user(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect('create_user')   

def modify_user(request, id):
    usuario = get_object_or_404(Usuario, id=id)#buscar personal

    data = {
        'form_usuario':UsuariolFrom(instance=usuario)
    }

    if request.method == 'POST':
        formulario = UsuariolFrom(data=request.POST, instance=usuario, files=request.FILES)#cargar formulario con el contexto y instance para pasarle la id
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect('create_user')

    return render(request, 'app/modify_user.html', data)   

def create_staff(request):
    personal = Personal.objects.order_by('-id')
    if request.method == 'POST':
        formulario = CustomUserCreationFrom(data=request.POST)
        
        from_personal = PersonalFrom(request.POST, request.FILES)

        if from_personal.is_valid():
            instance = from_personal.save(commit=False)
            instance.usuario_fk = request.user    #instancear usuario_fk con datos de user(datos usando en register)
            instance.save()
            user = instance.usuario_fk
            #Permisos
            permiso = request.POST.get('tipo_personal_fk')
            if permiso == '2':
                assign_role(user, 'externo') #asginar rol
                remove_role(user, 'moderador') #asginar rol
            elif  permiso == '3':
                assign_role(user, 'externo') #asginar rol
                remove_role(user, 'moderador') #asginar rol
            elif  permiso == '4':
                assign_role(user, 'productor') #asginar rol
                remove_role(user, 'moderador') #asginar rol   
            elif permiso == '5':
                assign_role(user, 'transportista') #asginar rol  
                remove_role(user, 'moderador') #asginar rol
            elif permiso == '6':
                assign_role(user, 'moderador') #asginar rol
            elif permiso == '7':
                assign_role(user, 'consultor') #asginar rol
                remove_role(user, 'moderador') #asginar rol
            messages.success(request, "Registro completo")
            remove_role(user, 'entrada')
         
            #correo eletronico
            subcjet = user.username #Nombre del contacto  
            message="Registro acceptado,hola" + " " + subcjet + " Tu solicitud de registro fue aceptada con exito, tus datos para iniciar session son:\nNombre de usuario: "+  subcjet + " \nContraseña: " + subcjet+request.POST.get('rut_personal')
            from_email = settings.EMAIL_HOST_USER #Email maipo grande
            recipient_list = [user.email]#Email a enviar el correo
            send_mail(subcjet, message, from_email, recipient_list)
            
            return redirect(index)
    else:
        from_personal = PersonalFrom
        
    return  render(request, 'app/create_staff.html',{'from_personal':from_personal,'personal':personal })    


@login_required 
@has_role_decorator('moderador')
def list_staff(request):
    personal = Personal.objects.order_by('-id')
    contexto = {'personal':personal}

    return  render(request, 'app/list_staff.html',contexto) 
     

@login_required 
@has_role_decorator('moderador')
def delete_staff(request, id):
    personal = get_object_or_404(Personal, id=id)
    personal.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect('/list_staff')

@login_required 
@has_role_decorator('moderador')
def modify_staff(request, id):
    
    personal = get_object_or_404(Personal, id=id)#buscar personal

    data = {
        'from_personal':PersonalFrom(instance=personal)
    }

    if request.method == 'POST':
        formulario = PersonalFrom(data=request.POST, instance=personal, files=request.FILES)#cargar formulario con el contexto y instance para pasarle la id
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect('create_staff')

    return render(request, 'app/modify_staff.html', data)

@login_required 
@has_role_decorator('productor')
def create_product(request):
    productos = producto.objects.order_by('-id')
    if request.method == 'POST':

        from_producto = PorductoFrom(request.POST, request.FILES)
        if from_producto.is_valid():
            instance = from_producto.save(commit=False)
            instance.usuario_fk = request.user    
            instance.save() 
            messages.success(request, "Producto Registrado")
            
            return redirect('create_product')

@login_required 
@has_role_decorator('productor')
def post_create_product(request):
    productos = desc_fruta.objects.order_by('-id')
    if request.method == 'POST':

        from_producto = Post_PorductoFrom(request.POST, request.FILES)
        if from_producto.is_valid():
            instance = from_producto.save(commit=False)
            instance.productor_fk = request.user    
            instance.save() 
            messages.success(request, "Producto registrado en inventario")
            
            return redirect('post_create_product')



    else:
        from_producto = Post_PorductoFrom
        
    return  render(request, 'app/post_create_product.html',{'from_producto':from_producto, 'productos':productos } )

@login_required 
@has_role_decorator('productor')
def list_product(request):

    productos = producto.objects.order_by('-id')
    contexto = {'productos':productos}
    return  render(request, 'app/list_product.html',contexto)


@login_required 
@has_role_decorator('productor')
def delete_product(request, id):
    Producto = get_object_or_404(producto, id=id)
    Producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect('create_product')


@has_role_decorator('productor')
@login_required 
def delete_post_product(request, id):
    Producto = get_object_or_404(desc_fruta, id=id)
    Producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect('post_create_product')

@login_required 
@has_role_decorator('productor')
def modify_product(request,id):
    Producto = get_object_or_404(producto, id=id)
    
    data = {
        'from_producto':PorductoFrom(instance=Producto)
    }

    if request.method == 'POST':
        formulario = PorductoFrom(data=request.POST, instance=Producto, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect('create_product')

    return render(request, 'app/modify_product.html', data)    

@has_role_decorator('productor')
@login_required 
def modify_post_product(request,id):
    Producto = get_object_or_404(desc_fruta, id=id)
    
    data = {
        'from_producto':Post_PorductoFrom(instance=Producto)
    }

    if request.method == 'POST':
        formulario = Post_PorductoFrom(data=request.POST, instance=Producto, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect('post_create_product')

    return render(request, 'app/modify_post_product.html', data)   


@login_required 
def my_sales(request):
  

    ventas = venta.objects.order_by('-id')
    

    return  render(request, 'app/my_sales.html',{'ventas':ventas })


@login_required 
def create_sale(request,id ):
    
    id_producto = get_object_or_404(producto, id=id)
    Producto = get_object_or_404(producto, id=id)
    ventas = venta.objects.order_by('-id')
    data = {
        'from_producto':Porducto_dps_ventaFrom(instance=Producto)
    }

    if request.method == 'POST':

        from_venta = ventaFrom(request.POST, request.FILES)
        
        if from_venta.is_valid():

            instance = from_venta.save(commit=False)
            instance.fk_producto = id_producto  
            instance.usuario_fk = request.user    
            instance.save() 

            formulario = Porducto_dps_ventaFrom(data=request.POST, instance=Producto, files=request.FILES)
            
            if formulario.is_valid():
            
                estado = "No Disponible"
                instance = formulario.save(commit=False)
                instance.usuario_fk = request.user 
                instance.estado_fk = producto_estado.objects.get(desc_estado=estado)
                instance.save() 

            messages.success(request, "Venta Creada")
            return redirect(mis_ventas)
    else:
        from_venta = ventaFrom
        
    return  render(request, 'app/create_sale.html',{'from_venta':from_venta, 'ventas':ventas} )

@login_required 
def list_sales(request):
    ventas = venta.objects.order_by('-id')
    contexto = {'ventas':ventas}

    return  render(request, 'app/list_sales.html',contexto)


login_required 
def delete_sales(request, id):
    ventas = get_object_or_404(venta, id=id)
    ventas.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect('list_sales')


@login_required 
def modify_sales(request,id):
    ventas = get_object_or_404(venta, id=id)

    data = {
        'from_venta':ventaModifcarFrom(instance=ventas)
    }

    if request.method == 'POST':
        formulario = ventaFrom(data=request.POST, instance=ventas, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect('list_sales')

    return render(request, 'app./modify_sales.html', data) 




