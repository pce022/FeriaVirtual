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
    desc_tipo_empresa = models.CharField(max_length=50, verbose_name = "Tipo empresa" )
    def __str__(self):
        return self.desc_tipo_empresa
    class Meta:     
        verbose_name = "Tipo de empresa"                                                                   
        verbose_name_plural = "Tipo de empresa"  


class Empresa(models.Model):
    razon_social_cliente = models.CharField(max_length=100,verbose_name ="Razon social")
    giro_cliente = models.CharField(max_length=180,verbose_name ="Giro de la empresa")
    replegal_cliente = models.CharField(max_length=50,verbose_name ="Representante legal")
    rut_empresa = models.CharField(max_length=10,verbose_name ="Rut de la empresa")
    tipo_empresa_fk = models.ForeignKey(Tipo_empresa, on_delete=models.CASCADE,unique=False,verbose_name ="Tipo de empresa")
    def __str__(self):
        return self.razon_social_cliente
    class Meta:  
        verbose_name = "Empresa"                                                                    
        verbose_name_plural = "Empresa"



#Staff
class Tipo_personal(models.Model):
    tipo_personal = models.CharField(max_length=50)
    def __str__(self):
        return self.tipo_personal
    class Meta:  
        verbose_name = "Rol personal"                                                                 
        verbose_name_plural = "Rol personal"


class Personal(models.Model):
    usuario_fk = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    rut_personal = models.CharField(max_length=10, verbose_name="Rut")
    movil_personal = models.CharField(max_length=11, verbose_name="Movil")
    pais_personal = CountryField(verbose_name="Seleccionar pais")
    cuidad_personal = models.CharField(max_length=100, verbose_name="Ciudad")
    direccion_personal = models.CharField(max_length=50, verbose_name="Dirección")
    profesion_personal = models.CharField(max_length=100, verbose_name="Profesión")
    sexo_personal = models.CharField( max_length =500, null= False , blank=False, choices=genero_choices, verbose_name="Seleccionar genero") 
    tipo_personal_fk = models.ForeignKey(Tipo_personal, on_delete=models.CASCADE,unique=False, verbose_name="Rol")

    def __str__(self):
        return self.rut_personal

    class Meta:  
        verbose_name = "Personal"                                                                 
        verbose_name_plural = "Personal"
    

#User
class Tipo_usuario(models.Model):
    tipo_usuario = models.CharField(max_length=50)
    def __str__(self):
        return self.tipo_usuario
    class Meta:  
        verbose_name = "Rol usuario"                                                                 
        verbose_name_plural = "Rol usuario"


class Perfil_usuario(models.Model):
    desc_perfil = models.CharField(max_length=30, verbose_name="Descripcion de perfil de usuario")
    def __str__(self):
        return self.desc_perfil
    class Meta:  
        verbose_name = "Perfil usuario"                                                                 
        verbose_name_plural = "Perfil usuario"


class Usuario(models.Model):

    email_usuario = models.EmailField(max_length=100,verbose_name="Email usuario")
    movil_usuario = models.CharField(max_length=100,verbose_name="Movil usuario")
    Tipo_usuario_fk = models.ForeignKey(Tipo_usuario,on_delete=models.CASCADE,unique=False,verbose_name="Tipo de usuario")
    Perfil_usuario_fk = models.ForeignKey(Perfil_usuario,on_delete=models.CASCADE,unique=False,verbose_name="Perfil de usuario")
    personal_id_fk = models.ForeignKey(Personal,default=None,on_delete=models.CASCADE,unique=False,related_name='+')

    class Meta:  
        verbose_name = "Usuario"                                                                 
        verbose_name_plural = "Usuario"


class desc_fruta(models.Model):
    nombre_fruta =  models.CharField( max_length =500, null= False , blank=False,verbose_name="Nombre producto")  
    kilos_fruta =  models.IntegerField( null= False , blank=False, default =1,verbose_name="Cantidad")
    medida_fruta = models.IntegerField( null= False , blank=False, default =1, choices=peso_choises,verbose_name="Tipo de medida" )
    valor_producto =  models.IntegerField(verbose_name="Valor producto")
    productor_fk = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Productor")

    def __str__(self):
        return self.nombre_fruta+ "" +self.kilos_fruta+ "" +self.medida_fruta+""

    class Meta:  
        verbose_name = "Descripcion producto"                                                                 
        verbose_name_plural = "Descripcion producto"


class producto_estado(models.Model):
    desc_estado =  models.CharField(max_length=120, verbose_name="Descripcion estado del producto" )
    def __str__(self):
        return self.desc_estado
    class Meta:  
        verbose_name = "Producto estado"                                                                 
        verbose_name_plural = "Producto estado"

                                    
class producto(models.Model):                                                             
    usuario_fk = models.ForeignKey(User,on_delete=models.CASCADE)                            
    nombre_producto= models.ForeignKey(desc_fruta,on_delete=models.CASCADE,unique=False, verbose_name = "Nombre de producto")
    origen_producto = models.CharField(max_length=30, verbose_name = "Origen del producto")
    estado_fk = models.ForeignKey(producto_estado,on_delete=models.CASCADE,unique=False, verbose_name = "Estado del")
    def __str__(self):
        return self.nombre_producto
    class Meta:
        permissions = (("create_record",  "Create product"),) 
        verbose_name = "Producto"                                                                 
        verbose_name_plural = "Producto"


#Solicitud
class frutas_espacio1(models.Model):
     
    fk_desc_fruta_espacio1= models.ForeignKey(desc_fruta,on_delete=models.CASCADE,unique=False)
    nombre_fruta_espacio1 = models.CharField(max_length=120, verbose_name = "Nombre producto (1)")
    def __str__(self):
        return self.nombre_fruta_espacio1
    class Meta:  
        verbose_name = "Producto 1"                                                                 
        verbose_name_plural = "Producto 1"


class frutas_espacio2(models.Model): 
    fk_desc_fruta_espacio2= models.ForeignKey(desc_fruta,on_delete=models.CASCADE, unique=False)
    nombre_fruta_espacio2 = models.CharField(max_length=120, verbose_name = "Nombre producto (2)")
    def __str__(self):
        return self.nombre_fruta_espacio2
    class Meta:  
        verbose_name = "Producto 2"                                                                 
        verbose_name_plural = "Producto 2"


class frutas_espacio3(models.Model):
    fk_desc_fruta_espacio3= models.ForeignKey(desc_fruta,on_delete=models.CASCADE,unique=False)
    nombre_fruta_espacio3 = models.CharField(max_length=120, verbose_name = "Nombre producto (3)")
    def __str__(self):
        return self.nombre_fruta_espacio3
    class Meta:  
        verbose_name = "Producto 3"                                                                 
        verbose_name_plural = "Producto 3"


class estado_productor_crear_solicitud(models.Model):
    estado_venta = models.CharField(max_length=120)

    def __str__(self):
        return self.estado_venta
    class Meta:  
        verbose_name = "Estado productor crear solicitud"                                                                 
        verbose_name_plural = "Estado productor crear solicitud"



class estado_solicitud(models.Model):
    desc_estado_solicitud = models.CharField(max_length=120, verbose_name = "Estado de solicitud")
    def __str__(self):
        return self.desc_estado_solicitud
    class Meta:  
        verbose_name = "Estado solicitud"                                                                 
        verbose_name_plural = "Estado solicitud"



class solicitud(models.Model):
    usuario_fk = models.ForeignKey(User,on_delete=models.CASCADE) 
    fk_estado_solicitud = models.ForeignKey(estado_solicitud, on_delete=models.CASCADE,unique=False)
    nombre_fruta_espacio1 = models.CharField( max_length =500, null= False , blank=False, verbose_name="Nombre producto (1)") 
    kilos_fruta_espacio1 = models.IntegerField( null= False , blank=False, default =1, verbose_name="Cantidad producto (1)")
    nombre_fruta_espacio2 = models.CharField( max_length =500, null= False , blank=False, verbose_name="Nombre producto (2)")  
    kilos_fruta_espacio2 = models.IntegerField( null= False , blank=False, default =1, verbose_name="Cantidad producto (2)")
    nombre_fruta_espacio3 = models.CharField( max_length =500, null= False , blank=False, verbose_name="Nombre producto (3)")   
    kilos_fruta_espacio3 = models.IntegerField( null= False , blank=False, default =1, verbose_name="Cantidad producto (3)")
    def __str__(self):
        return str(self.id)  
    class Meta:  
        verbose_name = "Solicitud"                                                                 
        verbose_name_plural = "Solicitud"
        
                                                                                                               
class productor_crear_solicitud(models.Model):
    usuario_fk = models.ForeignKey(User, on_delete=models.CASCADE) 
    fk_solicitud = models.ForeignKey(solicitud, on_delete=models.CASCADE)                             
    fk_estado_productor_crear_solicitud = models.ForeignKey(estado_productor_crear_solicitud, on_delete=models.CASCADE) 
    fk_frutas_espacio1= models.ForeignKey(frutas_espacio1,on_delete=models.CASCADE,unique=False,verbose_name="Nombre producto (1)")
    fk_frutas_espacio2= models.ForeignKey(frutas_espacio2,on_delete=models.CASCADE,unique=False,verbose_name="Nombre producto (2)")                                                                                                           
    fk_frutas_espacio3= models.ForeignKey(frutas_espacio3,on_delete=models.CASCADE,unique=False,verbose_name="Nombre producto (3)")
    def __str__(self):
        return str(self.id)
    class Meta:  
        verbose_name = "Productor crear solicitud"                                                                 
        verbose_name_plural = "Productor crear solicitud"


#Auction
class estado_subasta(models.Model):
    estado_subasta = models.CharField(max_length=120)
    def __str__(self):
        return self.estado_subasta
    class Meta:  
        verbose_name = "Estado subasta"                                                                 
        verbose_name_plural = "Estado subasta"

class pais(models.Model):
    name = CountryField(verbose_name = "Nombre pais" )
    def __str__(self):
        return self.name
    class Meta:  
        verbose_name = "Pais"                                                                 
        verbose_name_plural = "Pais"
    
class subasta(models.Model):
    fk_transportistaa_usuario = models.ForeignKey(User,on_delete=models.CASCADE) 
    fk_solicitud = models.ForeignKey(productor_crear_solicitud, on_delete=models.CASCADE)                             
    fk_estado_subasta = models.ForeignKey(estado_subasta,  on_delete=models.CASCADE) 
    mi_apuesta = models.IntegerField(verbose_name="Monto de apuesta")                                                                                                      
    fec_subasta =models.DateField(auto_now = True,verbose_name="Fecha de subasta")
    pais = CountryField(verbose_name="Pais")
    cuidad = models.CharField(max_length=120,verbose_name="Ciudad")                                       
    mi_direccion = models.CharField(max_length=120,verbose_name="Dirección")
    def __str__(self):
        return str(self.id)
    class Meta:  
        verbose_name = "Subasta"                                                                 
        verbose_name_plural = "Subasta"


#BID
class estado_venta(models.Model):
    estado_venta = models.CharField(max_length=120,verbose_name="Estado de venta")
    def __str__(self):
        return self.estado_venta
    class Meta:  
        verbose_name = "Estado de venta"                                                                 
        verbose_name_plural = "Estado de venta"

class venta(models.Model):
    fec_venta=models.DateField(auto_now = True, verbose_name="Fecha de venta")
    fk_estado_venta = models.ForeignKey(estado_venta,on_delete=models.CASCADE,unique=False)       
    usuario_fk = models.ForeignKey(User, on_delete=models.CASCADE)  
    fk_subasta = models.ForeignKey(subasta,on_delete=models.CASCADE) 
    def __str__(self):
        return str(self.id)
    class Meta:  
        verbose_name = "Venta"                                                                 
        verbose_name_plural = "Venta"


class boleta(models.Model):
    fec_boleta = models.DateField(auto_now = True, verbose_name="Fecha de boleta")  
    usuario_fk = models.ForeignKey(User,on_delete=models.CASCADE)  
    fk_venta = models.ForeignKey(venta,on_delete=models.CASCADE) 
    valor_transporte = models.IntegerField()
    valor_productos = models.IntegerField()
    valor_total =  models.IntegerField()
    class Meta:  
        verbose_name = "Boleta"                                                                 
        verbose_name_plural = "Boleta"



class mensaje_boleta(models.Model):                                
    mensaje = models.TextField(max_length=5000, verbose_name="Mensaje")
    usuario_fk = models.ForeignKey(User,on_delete=models.CASCADE)  
    class Meta:  
        verbose_name = "Mensaje boleta"                                                                 
        verbose_name_plural = "Mensaje boleta"



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
    
    def __str__(self):
        return self.nombre+ "" +self.apellido+ "" +self.tipo_personal_fk+""
    class Meta:  
        verbose_name = "Registro"                                                                 
        verbose_name_plural = "Registro"                                        


