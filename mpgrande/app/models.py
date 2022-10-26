from random import choices
from secrets import choice
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import AbstractUser, Permission, PermissionsMixin
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from .choices import*
from django.db import models

# Create your models here.


#Company
class Tipo_empresa(models.Model):

    desc_tipo_empresa = models.CharField(max_length=50)


    def __str__(self):
        return self.desc_tipo_empresa



class Empresa(models.Model):

    razon_social_cliente = models.CharField(max_length=100)
    giro_cliente = models.CharField(max_length=180)
    replegal_cliente = models.CharField(max_length=50)
    rut_empresa = models.CharField(max_length=10)
    tipo_empresa_fk = models.ForeignKey(Tipo_empresa, on_delete=models.CASCADE,unique=False)


#Staff

class Tipo_personal(models.Model):

    tipo_personal = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo_personal

class Personal(models.Model):
    usuario_fk = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    rut_personal = models.CharField(max_length=10)
    movil_personal = models.CharField(max_length=11)
    pais_personal = CountryField()
    cuidad_personal = models.CharField(max_length=100)
    direccion_personal = models.CharField(max_length=50)
    profesion_personal = models.CharField(max_length=100)
    sexo_personal = models.CharField( max_length =500, null= False , blank=False, choices=genero_choices) 
    tipo_personal_fk = models.ForeignKey(Tipo_personal,on_delete=models.CASCADE,unique=False)

    def __str__(self):
        return self.rut_personal
    

#User

class Tipo_usuario(models.Model):

    tipo_usuario = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo_usuario

class Perfil_usuario(models.Model):

    desc_perfil = models.CharField(max_length=30)

    def __str__(self):
        return self.desc_perfil

class Usuario(models.Model):

    email_usuario = models.EmailField(max_length=100)
    movil_usuario = models.CharField(max_length=100)
    Tipo_usuario_fk = models.ForeignKey(Tipo_usuario,on_delete=models.CASCADE,unique=False)
    Perfil_usuario_fk = models.ForeignKey(Perfil_usuario,on_delete=models.CASCADE,unique=False)
    personal_id_fk = models.ForeignKey(Personal,default=None,on_delete=models.CASCADE,unique=False,related_name='+')



#arreglar tipo estado
class desc_fruta(models.Model):
    nombre_fruta =  models.CharField( max_length =500, null= False , blank=False)  
    kilos_fruta =  models.IntegerField( null= False , blank=False, default =1)
    medida_fruta = models.IntegerField( null= False , blank=False, default =1, choices=peso_choises)
    valor_producto =  models.IntegerField()
    productor_fk = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return self.nombre_fruta+ "" +self.kilos_fruta+ "" +self.medida_fruta+""


class producto_estado(models.Model):
    desc_estado =  models.CharField(max_length=120)
    def __str__(self):
        return self.desc_estado

                                    
class producto(models.Model):                                                             
    usuario_fk = models.ForeignKey(User,on_delete=models.CASCADE,)                            
    nombre_producto= models.ForeignKey(desc_fruta,on_delete=models.CASCADE,unique=False)
    origen_producto = models.CharField(max_length=30)
    estado_fk = models.ForeignKey(producto_estado,on_delete=models.CASCADE,unique=False)
    def __str__(self):
        return self.nombre_producto
    class Meta:
        permissions = (("create_record",  "Create product"),) 


#Solicitud


class frutas_espacio2(models.Model):
     
    fk_desc_fruta_espacio2= models.ForeignKey(desc_fruta,on_delete=models.CASCADE, unique=False)
    nombre_fruta_espacio2 = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre_fruta_espacio2



class frutas_espacio1(models.Model):
     
    fk_desc_fruta_espacio1= models.ForeignKey(desc_fruta,on_delete=models.CASCADE,unique=False)
    nombre_fruta_espacio1 = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre_fruta_espacio1


class frutas_espacio3(models.Model):
     
    fk_desc_fruta_espacio3= models.ForeignKey(desc_fruta,on_delete=models.CASCADE,unique=False)
    nombre_fruta_espacio3 = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre_fruta_espacio3


class estado_productor_crear_solicitud(models.Model):
    estado_venta = models.CharField(max_length=120)

    def __str__(self):
        return self.estado_venta

class estado_solicitud(models.Model):
    desc_estado_solicitud = models.CharField(max_length=120)


    def __str__(self):
        return self.desc_estado_solicitud

class solicitud(models.Model):

    usuario_fk = models.ForeignKey(User,on_delete=models.CASCADE) 
    fk_estado_solicitud = models.ForeignKey(estado_solicitud, on_delete=models.CASCADE,unique=False)
    nombre_fruta_espacio1 = models.CharField( max_length =500, null= False , blank=False) 
    kilos_fruta_espacio1 = models.IntegerField( null= False , blank=False, default =1)
    nombre_fruta_espacio2 = models.CharField( max_length =500, null= False , blank=False)  
    kilos_fruta_espacio2 = models.IntegerField( null= False , blank=False, default =1)
    nombre_fruta_espacio3 = models.CharField( max_length =500, null= False , blank=False)   
    kilos_fruta_espacio3 = models.IntegerField( null= False , blank=False, default =1)


    def __str__(self):
        return str(self.id)  
        
                                                                                                               
class productor_crear_solicitud(models.Model):
    usuario_fk = models.ForeignKey(User, on_delete=models.CASCADE) 
    fk_solicitud = models.ForeignKey(solicitud, on_delete=models.CASCADE)                             
    fk_estado_productor_crear_solicitud = models.ForeignKey(estado_productor_crear_solicitud, on_delete=models.CASCADE) 
    fk_frutas_espacio1= models.ForeignKey(frutas_espacio1,on_delete=models.CASCADE,unique=False)
    fk_frutas_espacio2= models.ForeignKey(frutas_espacio2,on_delete=models.CASCADE,unique=False)                                                                                                           
    fk_frutas_espacio3= models.ForeignKey(frutas_espacio3,on_delete=models.CASCADE,unique=False)
    
    def __str__(self):
        return str(self.id)

#Auction
    
class estado_subasta(models.Model):
    estado_subasta = models.CharField(max_length=120)

    def __str__(self):
        return self.estado_subasta

class pais(models.Model):
    name = models.CharField(max_length=100)
    


class subasta(models.Model):
    fk_transportistaa_usuario = models.ForeignKey(User,on_delete=models.CASCADE) 
    fk_solicitud = models.ForeignKey(productor_crear_solicitud, on_delete=models.CASCADE)                             
    fk_estado_subasta = models.ForeignKey(estado_subasta,  on_delete=models.CASCADE) 
    mi_apuesta =   models.IntegerField()                                                                                                      
    fec_subasta =models.DateField(auto_now = True)
    pais = CountryField()
    cuidad = models.CharField(max_length=120)                                       
    mi_direccion = models.CharField(max_length=120)


    def __str__(self):
        return str(self.id)

#BID

class estado_venta(models.Model):
    estado_venta = models.CharField(max_length=120)

    def __str__(self):
        return self.estado_venta

class venta(models.Model):
    fec_venta=models.DateField(auto_now = True)
    fk_estado_venta = models.ForeignKey(estado_venta,on_delete=models.CASCADE,unique=False)       
    usuario_fk = models.ForeignKey(User, on_delete=models.CASCADE)  
    fk_subasta = models.ForeignKey(subasta,on_delete=models.CASCADE) 

    def __str__(self):
        return str(self.id)


class boleta(models.Model):

    fec_boleta = models.DateField(auto_now = True)  
    usuario_fk = models.ForeignKey(User,on_delete=models.CASCADE)  
    fk_venta = models.ForeignKey(venta,on_delete=models.CASCADE) 
    valor_transporte = models.IntegerField()
    valor_productos = models.IntegerField()
    valor_total =  models.IntegerField()

    
class mensaje_boleta(models.Model):
                                          
    mensaje = models.TextField(max_length=5000)
    usuario_fk = models.ForeignKey(User,on_delete=models.CASCADE)  

class mensaje_registro(models.Model):

    nombre = models.CharField(max_length=1000)
    apellido = models.CharField(max_length=1000)
    email_mensaje = models.EmailField()
    rut_personal = models.CharField(max_length=10)
    movil_personal = models.CharField(max_length=11)
    pais_personal = CountryField()
    cuidad_personal = models.CharField(max_length=100)
    direccion_personal = models.CharField(max_length=50)
    profesion_personal = models.CharField(max_length=100)
    sexo_personal = models.CharField(max_length =500, null= False , blank=False, choices=genero_choices) 
    mensaje = models.TextField(max_length=5000)
    tipo_personal_fk = models.CharField(max_length =500, null= False , blank=False, choices=user_choice)                                        


