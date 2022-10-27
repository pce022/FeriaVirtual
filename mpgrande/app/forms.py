import django
from django.forms import fields
from app.models import *
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CustomUserCreationFrom(UserCreationForm):

    class Meta:
        model = User  
        fields = ['username', 'email', 'password1', 'password2']
    pass

class StaffFrom(forms.ModelForm):
    class Meta:
        model = Personal 
        fields = (
            'rut_personal',
            'movil_personal',
            'pais_personal',
            'cuidad_personal',
            'direccion_personal',
            'profesion_personal',
            'sexo_personal',
            'tipo_personal_fk',
        )
    
class UserFrom(forms.ModelForm):
    class Meta:
        model = Usuario 
        fields = (
            
            'email_usuario',
            'movil_usuario',
            'Tipo_usuario_fk',
            'Perfil_usuario_fk',
            'personal_id_fk',

        )
        Labels = {

            'email_usuario': 'Email: ',
            'movil_usuario': 'Telefono',
            'Tipo_usuario_fk' :'Tipo de usuario: ',
            'Perfil_usuario_fk': 'Tipo de perfil: ',
            'personal_id_fk': 'Rut del personal',
        }        

class ProductFrom(forms.ModelForm):
    class Meta:
        model = producto
        fields = (
            'nombre_producto',
            'origen_producto',
            'estado_fk',
        )

class Post_ProductFrom(forms.ModelForm):
    class Meta:
        model = desc_fruta
        fields = (
            'nombre_fruta',
            'kilos_fruta',
            'medida_fruta',
            'valor_producto',
        )

class Post_product_saleFrom(forms.ModelForm):
    class Meta:
        model = producto
        fields = (
            
        )

class SaleFrom(forms.ModelForm):
    class Meta:
        model = venta
        fields = (
        )

class Sale_modifyFrom(forms.ModelForm):
    class Meta:
        model = venta
        fields = (
            'fk_estado_venta',
        )



class Request_from(forms.ModelForm):

    class Meta:
        model = solicitud
        fields = (
            'nombre_fruta_espacio1',
            'kilos_fruta_espacio1',
            'nombre_fruta_espacio2',
            'kilos_fruta_espacio2',
            'nombre_fruta_espacio3',
            'kilos_fruta_espacio3',
        )     

class Request_approve_from(forms.ModelForm):
    class Meta:
        model = solicitud
        fields = (

           'fk_estado_solicitud',
        )        

class Producer_create_requestFrom(forms.ModelForm):
    class Meta:
        model = productor_crear_solicitud
        fields = (
            
            'fk_frutas_espacio1',
            'fk_frutas_espacio2',
            'fk_frutas_espacio3',
        )  

class Approve_request_customer_producerForm(forms.ModelForm):
    class Meta:
        model = productor_crear_solicitud
        fields = (  )            
              
class Approve_request_customer_producerForm2(forms.ModelForm):
    class Meta:
        model = productor_crear_solicitud
        fields = (  )   

class AuctionForm(forms.ModelForm):
    class Meta:
        model = subasta
        fields = ('mi_apuesta',)  

class Auction_ParticipationForm(forms.ModelForm):     

    mi_apuesta = forms.IntegerField(min_value = 1, max_value= 10000000000)

    class Meta:
        model = subasta
        fields = ('mi_apuesta',)                          

class Start_auctionForm(forms.ModelForm):
    class Meta:
        model = subasta
        fields = (
            'pais',
            'cuidad',
            'mi_direccion',
        )             

class End_auctionForm(forms.ModelForm):

    class Meta:
        model = subasta
        fields = (  )        

class ticketForm(forms.ModelForm):

    class Meta:
        model = boleta
        fields = (  )          

class Sale_endForm(forms.ModelForm):

    class Meta:
        model = venta
        fields = (  )        

class confirm_deliveryForm(forms.ModelForm):
    class Meta:
        model = mensaje_boleta
        fields = (
            'mensaje',  
        )         

class Confirm_delivery_saleForm(forms.ModelForm):
    class Meta:
        model = venta
        fields = (  )            

class message_register_t(forms.ModelForm):

    class Meta:
        model = mensaje_registro
        fields = (

            'rut_personal',
            'nombre',
            'apellido',
            'email_mensaje',
            'movil_personal',
            'pais_personal',
            'cuidad_personal',
            'direccion_personal',
            'profesion_personal',
            'sexo_personal',
            'tipo_personal_fk',
            'mensaje',
            
        )             