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
    solicitudes =  solicitud.objects.order_by('-id')
    solicitudes2 = productor_crear_solicitud.objects.order_by('-id')
    subastas = productor_crear_solicitud.objects.order_by('-id')
    
    boletas2 = boleta.objects.order_by('-id')
    contexto = {'solicitudes':solicitudes}

    boletas = boleta.objects.count()
    total11 = 0
    total12 = 0
    year = datetime.now().year

    data11 = [] 
    data12 = [] 

    #enero
    for m in range(0,boletas): 
       
        if  boleta.objects.filter(fec_boleta__month=11):
            total11 = total11 +1

        else:
            total11 = 0
    
        data11.append((total11))
       
        if  boleta.objects.filter(fec_boleta__day=12):
            total12 = total12 +1

        else:
            tota2 = 0
    
        data12.append((total12))

    return  render(request, 'app/index.html',{'solicitudes':solicitudes, 'subastas':subastas,'solicitudes2':solicitudes2, 'boletas':boletas2,'data11':data11, 'data12':data12 })



@login_required
@has_role_decorator('moderador')
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

        form_usuario = UserFrom()
      
    else:
        form_usuario = UserFrom(request.POST)

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
        'form_usuario':UserFrom(instance=usuario)
    }

    if request.method == 'POST':
        formulario = UserFrom(data=request.POST, instance=usuario, files=request.FILES)#cargar formulario con el contexto y instance para pasarle la id
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect('create_user')

    return render(request, 'app/modify_user.html', data)   

@login_required 
@has_role_decorator('moderador')
def create_staff(request):
    personal = Personal.objects.order_by('-id')
    if request.method == 'POST':
        formulario = CustomUserCreationFrom(data=request.POST)
        
        from_personal = StaffFrom(request.POST, request.FILES)

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
        from_personal = StaffFrom
        
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
        'from_personal':StaffFrom(instance=personal)
    }

    if request.method == 'POST':
        formulario = StaffFrom(data=request.POST, instance=personal, files=request.FILES)#cargar formulario con el contexto y instance para pasarle la id
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

        from_producto = StaffFrom(request.POST, request.FILES)
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

        from_producto = Post_ProductFrom(request.POST, request.FILES)
        if from_producto.is_valid():
            instance = from_producto.save(commit=False)
            instance.productor_fk = request.user    
            instance.save() 
            messages.success(request, "Producto registrado en inventario")
            
            return redirect('post_create_product')



    else:
        from_producto = Post_ProductFrom
        
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
        'from_producto':ProductFrom(instance=Producto)
    }

    if request.method == 'POST':
        formulario = ProductFrom(data=request.POST, instance=Producto, files=request.FILES)
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
        'from_producto':Post_ProductFrom(instance=Producto)
    }

    if request.method == 'POST':
        formulario = Post_ProductFrom(data=request.POST, instance=Producto, files=request.FILES)
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
        'from_producto':Post_product_saleFrom(instance=Producto)
    }

    if request.method == 'POST':

        from_venta = SaleFrom(request.POST, request.FILES)
        
        if from_venta.is_valid():

            instance = from_venta.save(commit=False)
            instance.fk_producto = id_producto  
            instance.usuario_fk = request.user    
            instance.save() 

            formulario = Post_product_saleFrom(data=request.POST, instance=Producto, files=request.FILES)
            
            if formulario.is_valid():
            
                estado = "No Disponible"
                instance = formulario.save(commit=False)
                instance.usuario_fk = request.user 
                instance.estado_fk = producto_estado.objects.get(desc_estado=estado)
                instance.save() 

            messages.success(request, "Venta Creada")
            return redirect(my_sales)
    else:
        from_venta = SaleFrom
        
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
        'from_venta':Sale_modifyFrom(instance=ventas)
    }

    if request.method == 'POST':
        formulario = SaleFrom(data=request.POST, instance=ventas, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect('list_sales')

    return render(request, 'app/modify_sales.html', data) 


@login_required 
@has_role_decorator('externo')
def create_request(request):
    solicitudes = solicitud.objects.order_by('-id')
    if request.method == 'POST':

        from_solicitud = Request_from(request.POST, request.FILES)
        if from_solicitud.is_valid():
            estado = "Pendiente"
            instance = from_solicitud.save(commit=False)
            instance.usuario_fk = request.user
            instance.fk_estado_solicitud = estado_solicitud.objects.get(desc_estado_solicitud=estado)
                
            instance.save() 
            messages.success(request, "Solicitud creada a espera que un moderador la apruebe")
            
            return redirect('create_request')

    else:
        from_solicitud = Request_from
        
    return  render(request, 'app/create_request.html',{'from_solicitud':from_solicitud,'solicitudes':solicitudes } )


@login_required 
@has_role_decorator('productor') 
def producer_create_request(request,id):
    
    id_solicitud = get_object_or_404(solicitud, id=id)
    solicitudes = solicitud.objects.order_by('-id')

    productos = producto.objects.order_by('-id')
    if request.method == 'POST':

        from_solicitud = Producer_create_requestFrom(request.POST, request.FILES)
        if from_solicitud.is_valid():
            estado = "Pendiente"
            instance = from_solicitud.save(commit=False)
            instance.fk_solicitud = id_solicitud
            instance.usuario_fk = request.user
            instance.fk_estado_productor_crear_solicitud = estado_productor_crear_solicitud.objects.get(estado_venta=estado)
                
            instance.save() 


            #correo eletronico
                    
            email = id_solicitud.usuario_fk.email 
            subcjet = id_solicitud.usuario_fk.username #Nombre del contacto  
            message="El productor: " + str(request.user) + " creó  su solicitud de lote numero "+ str(id_solicitud.id)
            from_email = settings.EMAIL_HOST_USER #Email maipo grande
            recipient_list = [email]#Email a enviar el correo
            send_mail(subcjet, message, from_email, recipient_list)


            messages.success(request, "Lote creado a espera de la aprobacion del cliente")
            
            return redirect('listar_productor_solicitud')



    else:
        from_solicitud = Producer_create_requestFrom
        
    return  render(request, 'app/producer_create_request.html',{'from_solicitud':from_solicitud, 'solicitudes':solicitudes, 'productos':productos , 'id_solicitud':id_solicitud} )


@login_required 
@has_role_decorator('externo')
def modify_request(request,id):
    Solicitud = get_object_or_404(solicitud, id=id)
    
    data = {
        'from_solicitud':Request_from(instance=Solicitud)
    }

    if request.method == 'POST':
        formulario = Request_from(data=request.POST, instance=Solicitud, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            messages.success(request, "Modificado correctamente")

         
            return redirect('create_request')

            

    return render(request, 'app/modify_request.html', data) 


@has_role_decorator('moderador')    
@login_required 
def modify_request_status(request,id):
    Solicitud = get_object_or_404(solicitud, id=id)
    
    data = {
        'from_solicitud':Request_approve_from(instance=Solicitud)
    }

    if request.method == 'POST':
        formulario = Request_approve_from(data=request.POST, instance=Solicitud, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            messages.success(request, "Modificado correctamente")

            #correo eletronico

            email = Solicitud.usuario_fk.email 
            subcjet = Solicitud.usuario_fk.username #Nombre del contacto  
            estado = request.POST.get('fk_estado_solicitud')
            if estado == '2':
                message="Su solicitud " + str(Solicitud.id) + " fue aprobada"     

            if estado == '1':
                message="Su solicitud " + str(Solicitud.id) + " fue denegada"   

            from_email = settings.EMAIL_HOST_USER #Email maipo grande
            recipient_list = [email]#Email a enviar el correo
            send_mail(subcjet, message, from_email, recipient_list)
            return redirect('list_request')

    return render(request, 'app/modify_request.html', data)


@login_required 
@has_role_decorator('externo')
def delete_request(request,id):
    Solicitud = get_object_or_404(solicitud, id=id)
    Solicitud.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect('create_request')


@login_required 
def list_request(request):
    solicitudes = solicitud.objects.order_by('-id')
    contexto = {'solicitudes':solicitudes}

    return  render(request, 'app/list_request.html',contexto)    

@login_required 
def list_producer_request(request):
    solicitudes = productor_crear_solicitud.objects.order_by('-id')
    subastas = productor_crear_solicitud.objects.order_by('-id')
    contexto = {'solicitudes':solicitudes}

    return  render(request, 'app/list_producer_request.html',{'solicitudes':solicitudes, 'subastas':subastas})


@login_required 
def modify_list_producer_request(request,id):
    Solicitud = get_object_or_404(productor_crear_solicitud, id=id)
    
    data = {
        'from_solicitud':Producer_create_requestFrom(instance=Solicitud)
    }

    if request.method == 'POST':
        formulario = Producer_create_requestFrom(data=request.POST, instance=Solicitud, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect('list_producer_request')

    return render(request, 'app/modify_request.html', data) 


@login_required 
def delete_modify_list_producer_request(request,id):
    
    Solicitud = get_object_or_404(productor_crear_solicitud, id=id)
    Solicitud.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect('list_producer_request')


@has_role_decorator('externo')
@login_required 
def approve_producer_client_request(request,id):
    
    Solicitud = get_object_or_404(productor_crear_solicitud, id=id)
    Solicitud_id = get_object_or_404(productor_crear_solicitud, id=id)
    id_Solicitud = productor_crear_solicitud.objects.order_by('id')
    
    data = {
        'from_solicitud':Approve_request_customer_producerForm(instance=Solicitud)
    }

    if request.method == 'POST':

        formulario = Approve_request_customer_producerForm(data=request.POST, instance=Solicitud, files=request.FILES)

        if formulario.is_valid():
            instance = formulario.save(commit=False)

            instance.fk_estado_productor_crear_solicitud = estado_productor_crear_solicitud.objects.get(estado_venta="Aprobado")
            formulario.save()

            #Enviar email al cliente

            email = Solicitud.usuario_fk.email
            subcjet = Solicitud.usuario_fk.username
            message="Su solicitud número "+ str(Solicitud.id)+ " fue aprobada"
            from_email = settings.EMAIL_HOST_USER #Email maipo grande
            recipient_list = [email]#Email a enviar el correo
            send_mail(subcjet, message, from_email, recipient_list)

            messages.success(request, "Aprobado correctamente")
            return redirect('list_producer_request')

    return render(request, 'app/info_approve_request.html', {'from_solicitud':Approve_request_customer_producerForm(instance=Solicitud,),'id_Solicitud':id_Solicitud,'Solicitud_id':Solicitud_id })  


@has_role_decorator('externo')
@login_required 
def reject_producer_client_request(request,id):
    
    Solicitud = get_object_or_404(productor_crear_solicitud, id=id)
    Solicitud_id = get_object_or_404(productor_crear_solicitud, id=id)
    id_Solicitud = productor_crear_solicitud.objects.order_by('id')
    
    data = {
        'from_solicitud':Approve_request_customer_producerForm(instance=Solicitud)
    }

    if request.method == 'POST':
        formulario = Approve_request_customer_producerForm(data=request.POST, instance=Solicitud, files=request.FILES)
        if formulario.is_valid():
            instance = formulario.save(commit=False)

            instance.fk_estado_productor_crear_solicitud = estado_productor_crear_solicitud.objects.get(estado_venta="Rechazado")
            formulario.save()

            email = Solicitud.usuario_fk.email
            subcjet = Solicitud.usuario_fk.username
            message="Su solicitud número "+ str(Solicitud.id)+ " fue Rechazada"
            from_email = settings.EMAIL_HOST_USER #Email maipo grande
            recipient_list = [email]#Email a enviar el correo
            send_mail(subcjet, message, from_email, recipient_list)
            
            messages.success(request, "Rechazado correctamente")
            return redirect('list_producer_request')


    return render(request, 'app/info_approve_request.html', {'from_solicitud':Approve_request_customer_producerForm(instance=Solicitud,),'id_Solicitud':id_Solicitud,'Solicitud_id':Solicitud_id }) 


@login_required 
def participate_auction(request,id):
    
    Solicitud = get_object_or_404(productor_crear_solicitud, id=id)
    
    data = {
        'from_solicitud':AuctionForm(instance=Solicitud)
    }

    if request.method == 'POST':
        formulario = AuctionForm(data=request.POST, instance=Solicitud, files=request.FILES)
        if formulario.is_valid():
            estado = "Participando"
            instance = formulario.save(commit=False)

            instance.fk_estado_subasta = estado_subasta.objects.get(estado_subasta=estado)
           
            instance.fk_solicitud = Solicitud



            instance.fk_estado_solicitud = estado_solicitud.objects.get(desc_estado_solicitud=estado)
            messages.success(request, "Participando")
            return redirect('list_producer_request')

    return render(request, 'app/create_start_auction.html', data) 


@login_required 
def start_auction_participate(request,id):
    id_solicitud = get_object_or_404(productor_crear_solicitud, id=id)
    solicitud = get_object_or_404(productor_crear_solicitud, id=id)
    subastas = subasta.objects.order_by('id')

    solicitudes = productor_crear_solicitud.objects.order_by('-id')
   
    data = {
        'formulario':Approve_request_customer_producerForm2(instance=id_solicitud)
    }

    if request.method == 'POST':
        formulario = Start_auctionForm(request.POST, request.FILES)
        if formulario.is_valid():
            instance = formulario.save(commit=False)
            estado = "En curso"
            
            instance.fk_transportistaa_usuario = request.user
            instance.fk_solicitud = id_solicitud
            instance.fk_estado_subasta = estado_subasta.objects.get(estado_subasta=estado)            
            instance.mi_apuesta = 1
            instance.save() 

            formulario2 = Approve_request_customer_producerForm2(data=request.POST, instance=solicitud, files=request.FILES)
            
            if formulario2.is_valid():
                instance = formulario2.save(commit=False)
                estado = "Subasta en curso"
                
                instance.fk_estado_productor_crear_solicitud = estado_productor_crear_solicitud.objects.get(estado_venta=estado)   
                #instance.usuario_fk = request.user 
                instance.save() 
           
            messages.success(request, "Subasta creada")
            return redirect('list_producer_request')

    else:
        formulario = Start_auctionForm
    return render(request, 'app/create_start_auction.html',{'solicitudes':solicitudes,'id_solicitud':id_solicitud , 'formulario3':formulario,'formulario':aprobar_solicitud_cliente_productorForm2(instance=id_solicitud),'subastas':subastas } )  


@login_required 
def participate_auction_carrier(request,id,id_subasta) :   
     
    id_solicitud = get_object_or_404(productor_crear_solicitud, id=id)
    subasta_id = get_object_or_404(subasta, id=id_subasta)
   
    if request.method == 'POST':
        formulario = Auction_ParticipationForm(request.POST, request.FILES)
        if formulario.is_valid():
            instance = formulario.save(commit=False)
            estado = "Participando"
            instance.fk_estado_subasta = estado_subasta.objects.get(estado_subasta=estado)
            instance.fk_transportistaa_usuario = request.user
            instance.fk_solicitud = id_solicitud
            instance.pais = subasta_id.pais
            instance.cuidad = subasta_id.cuidad
            instance.mi_direccion = subasta_id.mi_direccion
            instance.save() 


            messages.success(request, "Participando en la subasta")

            #Enviar email al cliente

            email =id_solicitud.fk_solicitud.usuario_fk.email
            nombre =  request.user.username
            subcjet = id_solicitud.fk_solicitud.usuario_fk
            message="Un transportista ha participado en tu subasta número "+ str(subasta_id.id) + ", El transportista "+ nombre +" participó con $"+request.POST.get('mi_apuesta') +" pesos"
            from_email = settings.EMAIL_HOST_USER #Email maipo grande
            recipient_list = [email]#Email a enviar el correo
            
            send_mail(subcjet, message, from_email, recipient_list)

            return redirect('list_producer_request')

    else:
        formulario = Auction_ParticipationForm
    return render(request, 'app/create_start_auction.html',{'id_solicitud':id_solicitud , 'formulario':formulario} )
    

@login_required 
def end_auction(request, id,id2):
    id_subastas = get_object_or_404(subasta, id=id) #ID SUBASTA
    
    id_solicitud = get_object_or_404(productor_crear_solicitud, id=id2)#id solicitud_subasta
    solicitud = get_object_or_404(productor_crear_solicitud, id=id2)#id solicitud_subasta

    subastas = subasta.objects.order_by('id')

    data = {
        'formulario':Approve_request_customer_producerForm2(instance=id_solicitud)
    } 

    
    if request.method == 'POST':
        
        formulario = SaleFrom(request.POST, request.FILES)
        if formulario.is_valid():

            instance = formulario.save(commit=False)
            instance.fk_estado_venta = estado_venta.objects.get(estado_venta="Venta en curso")
            instance.usuario_fk = request.user
            instance.fk_subasta = id_subastas
            instance.save() 
            

            formulario2 = Approve_request_customer_producerForm2(data=request.POST, instance=solicitud, files=request.FILES)
            
            if formulario2.is_valid():
                instance = formulario2.save(commit=False)
                estado = "Subasta terminada"
                
                instance.fk_estado_productor_crear_solicitud = estado_productor_crear_solicitud.objects.get(estado_venta=estado)     
                #
                
                instance.save() 


                #EMAIL
                apuesta = request.POST.get('mi_apuesta')
                email=    id_subastas.fk_transportistaa_usuario.email
                subcjet = request.user.username


                message="La subasta de "+ subcjet +" con la id "+ str(solicitud.id) + " finalizo, Usted " + str(id_subastas.fk_transportistaa_usuario)+ " es el ganado con la apuesta de $"+ str(id_subastas.mi_apuesta)+ " pesos. " """
                Información de contacto del comprador """ +  """
                Nombre: """ + subcjet + """
                Email: """ + str(request.user.email)
                        

               
                from_email = settings.EMAIL_HOST_USER #Email maipo grande
                recipient_list = [email]#Email a enviar el correo
                
                send_mail(subcjet, message, from_email, recipient_list)


            messages.success(request, "Subasata Terminada, venta creada con exito")
            return redirect('list_producer_request')

    else:
        formulario = Auction_ParticipationForm
    return render(request, 'app./create_end_auction.html',{'id_solicitud':id_subastas , 'formulario':formulario, 'id_subastas':id_subastas,'subastas':subastas,'formulario':Approve_request_customer_producerForm2(instance=id_solicitud)  } )

@login_required 
def list_auction(request,id,nombreCliente,id_solicitud):
    id_solicitud2 = get_object_or_404(subasta, id=id)
    

    solicitudes = subasta.objects.order_by('-mi_apuesta')
    contexto = {'solicitudes':solicitudes}

    return  render(request, 'app/list_auction.html',{'id_solicitud2':id_solicitud2,'solicitudes':solicitudes, 'nombreCliente':nombreCliente,'id_solicitud':id_solicitud})  


@login_required 
def delete_auction(request,id):
    
    Solicitud = get_object_or_404(subasta, id=id)
    Solicitud.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect('list_auction')

@login_required 
def sales_list(request):
    ventas = venta.objects.order_by('-id')
    
    

    return  render(request, 'app/sales_list.html',{'ventas':ventas})


@login_required
def create_ticket(request,id):
    venta_id = get_object_or_404(venta, id=id) #ID SUBASTA
    solicitud = get_object_or_404(venta, id=id) #ID SUBASTA
    ventas = venta.objects.order_by('-id')

    data = {
        'formulario':Approve_request_customer_producerForm2(instance=venta_id)
    } 

    if request.method == 'POST':
        formulario = ticketForm(request.POST, request.FILES)
        if formulario.is_valid():

            instance = formulario.save(commit=False)
            instance.usuario_fk = request.user
            instance.fk_venta = venta_id
            instance.valor_transporte = venta_id.fk_subasta.mi_apuesta #valor tranposrte
            instance.valor_productos = venta_id.fk_subasta.fk_solicitud.fk_frutas_espacio1.fk_desc_fruta_espacio1.valor_producto + venta_id.fk_subasta.fk_solicitud.fk_frutas_espacio2.fk_desc_fruta_espacio2.valor_producto + venta_id.fk_subasta.fk_solicitud.fk_frutas_espacio3.fk_desc_fruta_espacio3.valor_producto
            instance.valor_total = venta_id.fk_subasta.mi_apuesta +   venta_id.fk_subasta.fk_solicitud.fk_frutas_espacio1.fk_desc_fruta_espacio1.valor_producto + venta_id.fk_subasta.fk_solicitud.fk_frutas_espacio2.fk_desc_fruta_espacio2.valor_producto + venta_id.fk_subasta.fk_solicitud.fk_frutas_espacio3.fk_desc_fruta_espacio3.valor_producto
            instance.save() 

            formulario2 = Sale_endForm(data=request.POST, instance=solicitud, files=request.FILES)
            if formulario2.is_valid():
                instance = formulario2.save(commit=False)
                estado = "Venta terminada"
 
                instance.fk_estado_venta = estado_venta.objects.get(estado_venta=estado)
                instance.usuario_fk = request.user     
                instance.save() 

                
                #email
                email=    venta_id.fk_subasta.fk_solicitud.usuario_fk.email
                subcjet = request.user.username
                message="Su lote "+ str(venta_id.fk_subasta.fk_solicitud.id)+ " Fue vendido/a a: "+ str(venta_id.usuario_fk) +" Para mas Información puede descargar la boleta con id de venta "+ str(venta_id.id)
                from_email = settings.EMAIL_HOST_USER #Email maipo grande
                recipient_list = [email]#Email a enviar el correo
                send_mail(subcjet, message, from_email, recipient_list)

                messages.success(request, "Boleta creada")
                return redirect('sales_list')



    else:
        formulario = ticketForm
    return render(request, 'app/create_ticket.html',{'venta_id':venta_id , 'ventas':ventas,'formulario':formulario,'formulario':Approve_request_customer_producerForm2(instance=venta_id) })  


@login_required
def list_ticket(request):

    boletas = boleta.objects.order_by('-id')
    return  render(request, 'app/list_ticket.html',{'boletas':boletas}) 


@login_required
def list_ticket_trans(request):

    boletas = boleta.objects.order_by('-id')
    return  render(request, 'app/list_ticket_trans.html',{'boletas':boletas}) 


@has_role_decorator('consultor')
@login_required
def list_ticket_producer(request):

    boletas = boleta.objects.order_by('-id')
    return  render(request, 'app/list_ticket_producer.html',{'boletas':boletas}) 


@login_required
def list_ticket_client(request):

    boletas = boleta.objects.order_by('-id')
    return  render(request, 'app/list_ticket.html',{'boletas':boletas}) 

@has_role_decorator('externo')
def confirm_delivery(request,id):
    Solicitud = get_object_or_404(venta, id=id)
    formulario = Confirm_delivery_saleForm
    formulario2 = confirm_deliveryForm

    data = {
        'from_solicitud':confirm_deliveryForm(instance=Solicitud)
    }


    if request.method == 'POST':

        formulario = Confirm_delivery_saleForm(data=request.POST, instance=Solicitud, files=request.FILES)
        formulario2 = confirm_deliveryForm(request.POST, request.FILES)

        if formulario.is_valid() :
            instance = formulario.save(commit=False)

            instance.fk_estado_venta = estado_venta.objects.get(estado_venta="Venta terminada")
            formulario.save()

            #Enviar email al cliente

            mensaje = request.POST.get('mensaje')

            email = Solicitud.fk_subasta.fk_solicitud.usuario_fk.email
            subcjet = request.user.username
            message="El pedido "+ str(Solicitud.id)+ " fue entregado correctamente a " +  str(request.user.username) + "\nMensaje: "+ "\n" +str(mensaje)
            from_email = settings.EMAIL_HOST_USER #Email maipo grande
            recipient_list = [email]#Email a enviar el correo
            send_mail(subcjet, message, from_email, recipient_list)

            messages.success(request, "Entrega confirmada correctamente")
            return redirect('sales_list')
    
      

    return render(request, 'app/confirm_order.html', {'from_solicitud':Approve_request_customer_producerForm(instance=Solicitud,), 'formulario2':formulario2, 'formulario':formulario } )  



def info_ticket(request,id):

    boletas_id = get_object_or_404(boleta, id=id) 
    boletas = boleta.objects.order_by('-id')
    return  render(request, 'app/info_ticket.html',{'boletas_id':boletas_id,'boletas':boletas}) 


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = producto.objects.all()
    serializer_class = ProductoSerializars


#pdf

class pdf_converterViews(View):
    def get(self,request,id):

        boletas_id = get_object_or_404(boleta, id=id) #ID SUBASTA
        
        boletas = boleta.objects.all()


        template = get_template('app/app.html')
        context ={

            'boletas':boletas,
            'boletas_id':boletas_id,
            'p.id':boletas_id,
            
            }
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="boleta_cliente.pdf"'

        #crear pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        #vali
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


class pdf_converterTransViews(View):
    def get(self,request,id):

        boletas_id = get_object_or_404(boleta, id=id) #ID SUBASTA
        
        boletas = boleta.objects.all()

        template = get_template('app/pdf_template_trans.html')
        context ={

            'boletas':boletas,
            'boletas_id':boletas_id,
            'p.id':boletas_id,
            
            }
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="boleta_transportista.pdf"'

        #crear pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        #vali
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response     

class pdf_converterProductorViews(View):
    def get(self,request,id):

        boletas_id = get_object_or_404(boleta, id=id) #ID SUBASTA
        
        boletas = boleta.objects.all()

        template = get_template('app/pdf_template_producer.html')
        context ={

            'boletas':boletas,
            'boletas_id':boletas_id,
            'p.id':boletas_id,
            
            }
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="boleta_productor.pdf"'

        #crear pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        #vali
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response             

@login_required
def graphics(request):
    boletas = boleta.objects.count()
    total11 = 0
    total12 = 0
    year = datetime.now().year
    data11 = [  ]
    data12 = [  ]

    #enero
    for m in range(0,boletas):

        data11 = [  ]    
       
        if  boleta.objects.filter(fec_boleta__month=11):
            total11 = total11 +1

        else:
            total11 = 0
    
        data11.append((total11))
       
        data12 = [  ]    
       
        if  boleta.objects.filter(fec_boleta__day=12):
            total12 = total12 +1

        else:
            tota2 = 0
    
        data12.append((total12))
    
    return  render(request, 'app/graphics.html',{'data11':data11, 'data12':data12} )


def graphics2(request):
    boletas = boleta.objects.all()
   
       
    return  render(request, 'app/graphics.html',{'boletas':boletas} ) 


@login_required
class grafico_dataViews(TemplateView):
    template_name = 'grafico.html'
   
    def get_grafico(self):
        data = [ ]
        year = datetime.now().year
        for m in range(1,13):
            total = boleta.objects.filter(fec_boleta__year=year, date__joined__month=m)
            data.append(float(total))
        return data     
    
    def get_context_data(self, ):
        context = super().get_context_data()
        context['panel'] = 'Panel de administrador'
        context['grafico'] = self.get_grafico()
        return context
