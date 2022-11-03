from django.contrib import admin
from app.models import *


class Personal_Admin(admin.ModelAdmin):
    list_display = ( "id", "usuario_fk", "rut_personal" , "movil_personal", "direccion_personal", "pais_personal",  "direccion_personal", "profesion_personal", "sexo_personal", "tipo_personal_fk") 

class Tipo_personalAdmin(admin.ModelAdmin):

    list_display = ( "id","tipo_personal")

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ( "id", "email_usuario","movil_usuario","Tipo_usuario_fk","personal_id_fk")   


class Tipo_usuarioAdmin(admin.ModelAdmin):
    list_display = ( "id", "tipo_usuario")     


class Perfil_usuarioAdmin(admin.ModelAdmin):
    list_display = ( "id", "desc_perfil")

class producto_estadoAdmin(admin.ModelAdmin):
    list_display = ( "id", "desc_estado") 

 
class productoAdmin(admin.ModelAdmin):
    list_display = ( "id", "usuario_fk","nombre_producto","origen_producto") 

class ventaAdmin(admin.ModelAdmin):
    list_display = ( "id", "fec_venta","fk_estado_venta","usuario_fk","fk_subasta") 

class estado_ventaAdmin(admin.ModelAdmin):
    list_display = ( "id", "estado_venta")

class desc_frutaAdmin(admin.ModelAdmin):
    list_display = ( "id", "kilos_fruta","kilos_fruta","productor_fk","valor_producto")   

class frutas_espacio1Admin(admin.ModelAdmin):
    list_display = ( "id", "fk_desc_fruta_espacio1","nombre_fruta_espacio1")   


class frutas_espacio2Admin(admin.ModelAdmin):
    list_display = ( "id", "fk_desc_fruta_espacio2","nombre_fruta_espacio2")   


class frutas_espacio3Admin(admin.ModelAdmin):
    list_display = ( "id", "fk_desc_fruta_espacio3","nombre_fruta_espacio3")  


class estado_solicitudAdmin(admin.ModelAdmin):
    list_display = ( "id", "desc_estado_solicitud")  

class solicitudAdmin(admin.ModelAdmin):
    list_display = ( "id", "usuario_fk", "nombre_fruta_espacio1", "kilos_fruta_espacio1", "nombre_fruta_espacio2", "kilos_fruta_espacio2", "nombre_fruta_espacio3", "kilos_fruta_espacio3")  

class estado_productor_crear_solicitudAdmin(admin.ModelAdmin):
    list_display = ( "id", "estado_venta") 


class productor_crear_solicitudAdmin(admin.ModelAdmin):
    list_display = ( "id", "usuario_fk", "fk_estado_productor_crear_solicitud", "fk_frutas_espacio1", "fk_frutas_espacio2", "fk_frutas_espacio3") 

class estado_productor_crear_solicitudAdmin(admin.ModelAdmin):
    list_display = ( "id", "estado_venta")

class estado_productor_crear_solicitudAdmin(admin.ModelAdmin):
    list_display = ( "id", "estado_venta")    

class estado_subastaAdmin(admin.ModelAdmin):
    list_display = ( "id", "estado_subasta")  


class subastaAdmin(admin.ModelAdmin):
    list_display = ( "id", "fk_transportistaa_usuario", "fk_solicitud", "fk_estado_subasta", "mi_apuesta","fec_subasta", "pais", "cuidad", "mi_direccion")  

class boletaAdmin(admin.ModelAdmin):
    list_display = ( "id", "fec_boleta", "usuario_fk", "fk_venta", "valor_transporte","valor_productos","valor_total")  


admin.site.register(Personal, Personal_Admin)  
admin.site.register(Tipo_personal, Tipo_personalAdmin) 
admin.site.register(Usuario, UsuarioAdmin) 
admin.site.register(Tipo_usuario, Tipo_usuarioAdmin) 
admin.site.register(Perfil_usuario, Perfil_usuarioAdmin) 
admin.site.register(producto_estado, producto_estadoAdmin) 
admin.site.register(producto, productoAdmin) 
admin.site.register(venta, ventaAdmin) 
admin.site.register(estado_venta, estado_ventaAdmin)
admin.site.register(desc_fruta, desc_frutaAdmin) 
admin.site.register(frutas_espacio1, frutas_espacio1Admin)    
admin.site.register(frutas_espacio2, frutas_espacio2Admin)   
admin.site.register(frutas_espacio3, frutas_espacio3Admin)     
admin.site.register(estado_solicitud, estado_solicitudAdmin) 
admin.site.register(solicitud, solicitudAdmin) 
admin.site.register(productor_crear_solicitud, productor_crear_solicitudAdmin) 
admin.site.register(estado_productor_crear_solicitud, estado_productor_crear_solicitudAdmin)  
admin.site.register(subasta, subastaAdmin)     
admin.site.register(estado_subasta, estado_subastaAdmin)
admin.site.register(boleta, boletaAdmin)